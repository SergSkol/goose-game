import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random

def create_enemy () :
  enemy = pygame.Surface(ENEMY_SIZE)
  enemy.fill(ENEMY_COLOR)
  enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *ENEMY_SIZE)
  enemy_move_left = [random.randint(-ENEMY_SPEED, -1), 0]
  return [enemy, enemy_rect, enemy_move_left]

def create_bonus () :
  bonus = pygame.Surface(BONUS_SIZE)
  bonus.fill(BONUS_COLOR)
  bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *BONUS_SIZE)
  bonus_move_bottom = [0, 1]
  return [bonus, bonus_rect, bonus_move_bottom]

pygame.init()

HEIGHT = 640
WIDTH = 1280
BACKGROUND_COLOR = (0, 0, 0)
FPS = 640

PLAYER_SIZE = (20, 20)
PLAYER_COLOR = (255, 255, 255)

ENEMY_SIZE = (30, 30)
ENEMY_COLOR = (255, 0, 0)
ENEMY_SPEED = 2
ENEMY_CREATE_INTERVAL = 1500

BONUS_SIZE = (40, 40)
BONUS_COLOR = (0, 255, 0)
BONUS_SPEED = 1
BONUS_CREATE_INTERVAL = 1000

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, ENEMY_CREATE_INTERVAL)
enemies = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, BONUS_CREATE_INTERVAL)
bonuses = []

main_display = pygame.display.set_mode( (WIDTH, HEIGHT) )
main_display.fill( BACKGROUND_COLOR )
main_display_fps = pygame.time.Clock()

player = pygame.Surface(PLAYER_SIZE)
player.fill(PLAYER_COLOR)
player_rect = player.get_rect()
player_move_down = [0, 1]
player_move_up = [0, -1]
player_move_left = [-1, 0]
player_move_right = [1, 0]

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
  
  main_display.fill(BACKGROUND_COLOR)

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
    
  for bonus in bonuses :
    my_bonus = bonus[0]
    my_bonus_rect = bonus[1]
    my_bonus_move = bonus[2]
    bonus[1] = my_bonus_rect.move(my_bonus_move)
    main_display.blit(my_bonus, my_bonus_rect)
    
  main_display.blit(player, player_rect)
  
  pygame.display.flip()
  
  for enemy in enemies :
    my_enemy_rect = enemy[1]
    if my_enemy_rect.left < 0 :
      enemies.pop(enemies.index(enemy))
  
  for bonus in bonuses :
    my_bonus_rect = bonus[1]
    if my_bonus_rect.bottom > HEIGHT :
      bonuses.pop(bonuses.index(bonus))