import pygame
import sys
import random
from player import Player
import wall
from camera import Camera
from enemy import Enemy
import settings


pygame.init()

world_walls = wall.generate_linear_dungeon()

#Setting screen and clock
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("AI Game")
clock = pygame.time.Clock()
camera = Camera()

#Setting player and enemy attributes
player = Player(20, settings.WORLD_HEIGHT - 60)
enemys = [
    Enemy(300,settings.WORLD_HEIGHT - 60),
    Enemy(500,settings.WORLD_HEIGHT - 60),
    Enemy(1500,settings.WORLD_HEIGHT - 60)
]

# Main game loop
while True:
    #for exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    camera.update(player)
    
    #player movement
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_SPACE]:
        dy = -1
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    player.move(dx,dy,world_walls)

    for enemy in enemys:
        enemy.chase(player, world_walls)
    # world_boundary = pygame.Rect(0, 0, settings.WORLD_WIDTH, settings.WORLD_HEIGHT)

    #Setting Game Up
    screen.fill((20,20,30))

    for wall in world_walls:
        draw_rect = camera.apply(wall.rect)
        pygame.draw.rect(screen, (50, 90, 110), draw_rect)

    player_draw_rect = camera.apply(player.rect)
    for enemy in enemys:
        enemy_draw_rect = camera.apply(enemy.rect)
        pygame.draw.rect(screen,enemy.color, enemy_draw_rect)
    pygame.draw.rect(screen, player.color, player_draw_rect)
    pygame.display.flip()
    clock.tick(60)

