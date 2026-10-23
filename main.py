import pygame
import sys
import random
from player import Player
import settings
pygame.init()


def generate_linear_dungeon():
     walls = []
    
     for room_index in range(settings.NUM_ROOMS):

        #First we calculate the base X offset 
        room_start_x =  room_index * settings.ROOM_WIDTH

        walls.append(pygame.Rect(room_start_x, 0, settings.ROOM_WIDTH, 20))
        walls.append(pygame.Rect(room_start_x, settings.ROOM_HEIGHT - 20, settings.ROOM_WIDTH, 20))

        if room_index > 0:
            walls.append(pygame.Rect(room_start_x, 0, 20, 180))
            walls.append(pygame.Rect(room_start_x, 320, 20, 180))

        else:
            walls.append(pygame.Rect(room_start_x, 0, 20, settings.ROOM_HEIGHT))

        if room_index < settings.NUM_ROOMS - 1:
            walls.append(pygame.Rect(room_start_x + settings.ROOM_WIDTH - 20, 0, 20, 180))     # Top-right post
            walls.append(pygame.Rect(room_start_x + settings.ROOM_WIDTH - 20, 320, 20, 180))   # Bottom-right post
        else:
            walls.append(pygame.Rect(room_start_x + settings.ROOM_WIDTH - 20, 0, 20, settings.ROOM_HEIGHT))

        layout_choice = random.choice(["pillars","barriers","empty"])

        if layout_choice == "pillars":
            # Add two pillars inside the room
            walls.append(pygame.Rect(room_start_x + 250, 150, 60, 200))
            walls.append(pygame.Rect(room_start_x + 500, 150, 60, 200))
            
        elif layout_choice == "barriers":
            # Add horizontal barricades forcing up/down movement
            walls.append(pygame.Rect(room_start_x + 300, 100, 200, 40))
            walls.append(pygame.Rect(room_start_x + 300, 360, 200, 40))

     return walls
        
world_walls = generate_linear_dungeon()

#Setting screen and clock

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("AI Game")
clock = pygame.time.Clock()


#Setting player and enemy attributes
# goes x y width height
player_rect = pygame.Rect(400,300,40,40)
player = Player(50, 50)
player_speed = 5
wall_rect = pygame.Rect(300,200,200,40)
enemy_rect = pygame.Rect(400,300,40,40)
enemy_speed = 2


# Main game loop
while True:
    #for exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    #player movement
    keys = pygame.key.get_pressed()
    dx = 0
    dy = 0
    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    player.move(dx,dy)
    
    for wall in world_walls:
       if player.rect.colliderect(wall):
           player.wall_collision(wall)
    world_boundary = pygame.Rect(0, 0, settings.WORLD_WIDTH, settings.WORLD_HEIGHT)
    player.rect.clamp_ip(world_boundary)


    #enemy movement
    enemy_dx = 0
    if enemy_rect.x < player_rect.x:
        enemy_dx = enemy_speed
    elif enemy_rect.x > player_rect.x:
        enemy_dx = -enemy_speed

    # Move X and check wall collision
    enemy_rect.x += enemy_dx
    for wall in world_walls:
        if enemy_rect.colliderect(wall):
            if enemy_dx > 0:
                enemy_rect.right = wall.left
            elif enemy_dx < 0:
                enemy_rect.left = wall.right

    #Calculate vertical movement toward player
    enemy_dy = 0
    if enemy_rect.y < player_rect.y:
        enemy_dy = enemy_speed
    elif enemy_rect.y > player_rect.y:
        enemy_dy = -enemy_speed

    # Move Y and check wall collision
    enemy_rect.y += enemy_dy
    for wall in world_walls:
        if enemy_rect.colliderect(wall):
            if enemy_dy > 0:
                enemy_rect.bottom = wall.top
            elif enemy_dy < 0:
                enemy_rect.top = wall.bottom

    if enemy_rect.colliderect(player_rect):
         player_rect.x = 50
         player_rect.y = 50
         enemy_rect.x = 300
         enemy_rect.y = 300


    #setting camera to match player position   
    camera_x = player_rect.x - settings.SCREEN_WIDTH // 2
    camera_y = player_rect.y - settings.SCREEN_HEIGHT // 2

    camera_x = max(0, min(camera_x, settings.WORLD_WIDTH - settings.SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, settings.WORLD_HEIGHT - settings.SCREEN_HEIGHT))


    #Setting Game Up
    screen.fill((20,20,30))

    for wall in world_walls:
        draw_wall = wall.copy()
        draw_wall.x -= camera_x
        draw_wall.y -= camera_y
        pygame.draw.rect(screen, (80, 90, 110), draw_wall)

    draw_player = player_rect.copy()
    draw_player.x -= camera_x
    draw_player.y -= camera_y

    draw_enemy = enemy_rect.copy()
    draw_enemy.x -= camera_x
    draw_enemy.y -= camera_y


    pygame.draw.rect(screen, (255,0, 0), draw_enemy)
    pygame.draw.rect(screen, (0, 128, 255), player.rect)
    pygame.display.flip()
    clock.tick(60)

