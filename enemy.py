import pygame
from entity import Entity
import random

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, damage=15, speed=3, y_velocity = 0, direction="LEFT", attack_range=30, attack_cooldown=1000, is_grounded=True, gravity = 0.8, color=(255,0,0))

    
    def update_ai(self, player, walls, enemies):
        # 1. Figure out which direction to face to look at the player
        if player.rect.centerx < self.rect.centerx:
            self.direction = "LEFT"
        else:
            self.direction = "RIGHT"

        # 2. Calculate horizontal distance between the RECTANGLES
        # This tells us exactly how many pixels of empty space are between them
        if self.direction == "LEFT":
            distance = self.rect.left - player.rect.right
        else:
            distance = player.rect.left - self.rect.right

        # 3. Handle movement AI (If not close enough, move toward player)
        dx = 0
        dy = 0  # Gravity handles vertical movement, but we initialize dy for your function
        
        # If there is still a gap, set movement direction towards the player
        if distance > 10:
            dx = -1 if self.direction == "LEFT" else 1

        # 5. SOLID OBJECT COLLISIONS (Combine Everything!)
        # Get all other living enemies (skipping this specific enemy)
        check_distance = 15
        prediction_rect = pygame.Rect(0, self.rect.bottom - 10, check_distance, 5)
        
        if self.direction == "RIGHT":
            prediction_rect.x = self.rect.right
        else:
            prediction_rect.x = self.rect.left - check_distance

        # Check if their path is blocked by any wall or entity
        path_is_blocked = False
        for wall in walls:
            if prediction_rect.colliderect(wall.rect):
                path_is_blocked = True
                break

        # If they are on the ground and running into an obstacle (or if you are standing above them), JUMP!
        # (We trigger the jump by passing a dy value or matching your player's jump physics logic)
        if path_is_blocked and self.is_grounded:
            dy = -1 # This triggers the "if dy != 0 and self.is_grounded:" logic inside your move function!
        elif player.rect.bottom < self.rect.top - 20 and self.is_grounded and random.random() < 0.02:
            # Optional: Small random chance to jump if the player is standing directly on a platform above them
            dy = -1

        # 5. SOLID OBJECT COLLISIONS
        other_enemies = [e for e in enemies if e != self and e.health > 0]
        obstacles = walls + [player] + other_enemies

        # 6. Pass everything to your parent Entity move function
        # Your move function will automatically apply 'y_velocity = 15 * dy' and handle gravity!
        self.move(dx, dy, obstacles)

        # 7. COMBAT CONDITION CHECK
        if distance <= self.attack_range:
            self.execute_strike([player])
