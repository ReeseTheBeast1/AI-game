import pygame
import sys
import random
from player import Player
from wall import generate_linear_dungeon
from camera import Camera
from enemy import Enemy
import settings

pygame.init()

world_walls = generate_linear_dungeon()

# Setting screen and clock
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("AI Game")
clock = pygame.time.Clock()
camera = Camera()

# Setup font for the game over screen
pygame.font.init()
game_font = pygame.font.SysFont("Arial", 40)

# Setting player and enemy attributes
player = Player(20, settings.WORLD_HEIGHT - 60)
enemys = [
    Enemy(300, settings.WORLD_HEIGHT - 60),
    Enemy(500, settings.WORLD_HEIGHT - 60),
    Enemy(1500, settings.WORLD_HEIGHT - 60)
]

# Track the game over state
game_over = False

# Main game loop
while True:
    # for exiting and restarts
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # 🎯 Listen for restart input if the player is dead
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset map, player, and enemies back to starting states
                world_walls = generate_linear_dungeon()
                player = Player(20, settings.WORLD_HEIGHT - 60)
                enemys = [
                    Enemy(300, settings.WORLD_HEIGHT - 60),
                    Enemy(500, settings.WORLD_HEIGHT - 60),
                    Enemy(1500, settings.WORLD_HEIGHT - 60)
                ]
                game_over = False

    # Setting Game Up (Clear screen first)
    screen.fill((20, 20, 30))

    # Always draw the world walls regardless of state
    for wall in world_walls:
        draw_rect = camera.apply(wall.rect)
        pygame.draw.rect(screen, (50, 90, 110), draw_rect)

    # 🎯 GAMEPLAY STATE
    if not game_over:
        camera.update(player)
        
        # player movement
        player.update(world_walls, enemys)
        player.get_vision_rect(100)
        player.check_enemies_in_front(enemys, distance=100)
            
        for enemy in enemys:
            enemy.update_ai(player, world_walls, enemys)

            if enemy.health <= 0:
                enemys.remove(enemy)
                
        # Check if player died this frame
        if player.health <= 0:
            game_over = True

        # Draw characters normally while alive
        player_draw_rect = camera.apply(player.rect)
        for enemy in enemys:
            enemy_draw_rect = camera.apply(enemy.rect)
            pygame.draw.rect(screen, enemy.color, enemy_draw_rect)
        pygame.draw.rect(screen, player.color, player_draw_rect)

    # 💀 GAME OVER STATE
    else:
        # Create text surfaces to display over the map
        text_surface = game_font.render("GAME OVER", True, (255, 50, 50))
        restart_surface = game_font.render("Press 'R' to Restart", True, (255, 255, 255))
        
        # Center the text calculations based on screen dimensions
        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 30))
        restart_rect = restart_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 30))
        
        # Blit (draw) the text surfaces onto the screen
        screen.blit(text_surface, text_rect)
        screen.blit(restart_surface, restart_rect)

    pygame.display.flip()
    clock.tick(60)