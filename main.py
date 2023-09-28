import pygame
from pygame.constants import QUIT

pygame.init()

HEIGHT = 640
WIDTH = 1280
BACKGROUND_COLOR = (0, 100, 100)
PLAYER_COLOR = (255, 255, 255)
PLAYER_SIZE = (20, 20)
FPS = 240

main_display = pygame.display.set_mode( (WIDTH, HEIGHT) )
main_display.fill( BACKGROUND_COLOR )
main_display_fps = pygame.time.Clock()

player = pygame.Surface(PLAYER_SIZE)
player.fill(PLAYER_COLOR)
player_rect = player.get_rect()
player_speed = [1, 1]

playing = True
while playing :
  main_display_fps.tick(FPS)
  for event in pygame.event.get() :
    if event.type == QUIT :
      playing = False
  
  if player_rect.right > WIDTH or player_rect.left < 0 :
    player_speed[0] = -player_speed[0]
    
  if player_rect.bottom > HEIGHT or player_rect.top < 0 :
    player_speed[1] = -player_speed[1]
  
  main_display.fill(BACKGROUND_COLOR)
  main_display.blit(player, player_rect)
  player_rect = player_rect.move(player_speed)
  
  pygame.display.flip()