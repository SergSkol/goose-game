import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
import os

def create_enemy () :
  enemy = pygame.image.load('img/enemy.png').convert_alpha()
  enemy_height = enemy.get_height()
  enemy_rect = pygame.Rect(WIDTH, 
                           random.randint(enemy_height, HEIGHT - enemy_height), 
                           *enemy.get_size())
  enemy_move_left = [random.randint(-ENEMY_SPEED, -PLAYER_SPEED), 0]
  return [enemy, enemy_rect, enemy_move_left]

def create_bonus () :
  bonus = pygame.image.load('img/bonus.png').convert_alpha()
  bonus_width = bonus.get_width()
  bonus_rect = pygame.Rect(random.randint(bonus_width, WIDTH - bonus_width), 
                           -bonus.get_height(), 
                           *bonus.get_size())
  bonus_move_bottom = [0, random.randint(PLAYER_SPEED, ENEMY_SPEED)]
  return [bonus, bonus_rect, bonus_move_bottom]

pygame.init()

HEIGHT = 640
WIDTH = 1280
FPS = 640
FONT = pygame.font.SysFont('Verdana', 20)

PLAYER_SPEED = 4
PLAYER_IMAGE_PATH = "img/goose"
PLAYER_IMAGES = os.listdir(PLAYER_IMAGE_PATH)
CHANGE_PLAYER_IMAGE_INTERVAL = 200

SCORE_COLOR = (0, 0, 0)

ENEMY_SPEED = 8
ENEMY_CREATE_INTERVAL = 1500

BONUS_SPEED = 1
BONUS_CREATE_INTERVAL = 1000

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, ENEMY_CREATE_INTERVAL)
enemies = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, BONUS_CREATE_INTERVAL)
bonuses = []

CHANGE_PLAYER_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_PLAYER_IMAGE, CHANGE_PLAYER_IMAGE_INTERVAL)
player_image_index = 0

main_display = pygame.display.set_mode( (WIDTH, HEIGHT) )
main_display_bg = pygame.transform.scale(pygame.image.load('img/background.png'), (WIDTH, HEIGHT) )
main_display_bg_x1 = 0
main_display_bg_x2 = main_display_bg.get_width()
main_display_bg_move = 3

main_display_fps = pygame.time.Clock()

player = pygame.image.load('img/player.png')
player_rect = player.get_rect()
player_rect.center = main_display.get_rect().center
player_move_down = [0, PLAYER_SPEED]
player_move_up = [0, -PLAYER_SPEED]
player_move_left = [-PLAYER_SPEED, 0]
player_move_right = [PLAYER_SPEED, 0]

score = 0
playing = True

while playing :
  main_display_fps.tick(FPS)
  for event in pygame.event.get() :
    if event.type == QUIT :
      playing = False
    elif event.type == CREATE_ENEMY :
      enemy = create_enemy()
      enemies.append(enemy)
    elif event.type == CREATE_BONUS :
      bonus = create_bonus()
      bonuses.append(bonus)
    elif event.type == CHANGE_PLAYER_IMAGE :
      player = pygame.image.load(os.path.join(PLAYER_IMAGE_PATH, PLAYER_IMAGES[player_image_index])).convert_alpha()
      player_image_index += 1
      if player_image_index >= len(PLAYER_IMAGES) :
        player_image_index = 0

  main_display_bg_x1 -= main_display_bg_move
  main_display_bg_x2 -= main_display_bg_move
  
  if main_display_bg_x2 < 0:
    main_display_bg_x1 = 0
    main_display_bg_x2 = main_display_bg.get_width()
  
  main_display.blit(main_display_bg, (main_display_bg_x1, 0) )
  main_display.blit(main_display_bg, (main_display_bg_x2, 0) )

  keys = pygame.key.get_pressed()
  
  if keys[K_DOWN] and player_rect.bottom < HEIGHT :
    player_rect = player_rect.move(player_move_down)
    
  if keys[K_RIGHT] and player_rect.right < WIDTH :
    player_rect = player_rect.move(player_move_right)

  if keys[K_UP] and player_rect.top > 0 :
    player_rect = player_rect.move(player_move_up)
    
  if keys[K_LEFT] and player_rect.left > 0 :
    player_rect = player_rect.move(player_move_left)

  for enemy in enemies :
    my_enemy = enemy[0]
    my_enemy_rect = enemy[1]
    my_enemy_move = enemy[2]
    enemy[1] = my_enemy_rect.move(my_enemy_move)
    main_display.blit(my_enemy, my_enemy_rect)
    
    if player_rect.colliderect(my_enemy_rect):
      playing = False
    
  for bonus in bonuses :
    my_bonus = bonus[0]
    my_bonus_rect = bonus[1]
    my_bonus_move = bonus[2]
    bonus[1] = my_bonus_rect.move(my_bonus_move)
    main_display.blit(my_bonus, my_bonus_rect)
    
    if player_rect.colliderect(my_bonus_rect):
      score += 1
      bonuses.pop(bonuses.index(bonus))
    
  main_display.blit(FONT.render(str(score), True, SCORE_COLOR), (WIDTH-50, 20))
  main_display.blit(player, player_rect)
  
  pygame.display.flip()
  
  for enemy in enemies :
    my_enemy_rect = enemy[1]
    if my_enemy_rect.right < 0 :
      enemies.pop(enemies.index(enemy))
  
  for bonus in bonuses :
    my_bonus_rect = bonus[1]
    if my_bonus_rect.bottom > HEIGHT :
      bonuses.pop(bonuses.index(bonus))