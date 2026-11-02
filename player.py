import pygame
from entity import Entity


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, damage=15, speed=5, y_velocity = 0, direction="RIGHT", attack_range=30,  attack_cooldown=500, is_grounded=True, gravity = 0.8, color=(0,128,255))
        self.mouse_was_released = True
    def update(self, walls, enemies):

        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_SPACE]:
            dy = -1
        if keys[pygame.K_a]:
            dx = -1
            self.direction = "LEFT"
        if keys[pygame.K_d]:
            self.direction = "RIGHT"
            dx = 1
        if click[0]:  # Left Click
            if self.mouse_was_released:
                # Condition met! Execute the parent's combat logic
                self.execute_strike(enemies)
                self.mouse_was_released = False
        else:
            self.mouse_was_released = True
        enemy_rects = [enemy for enemy in enemies if enemy.health > 0]
        obstacles = walls + enemy_rects
        self.move(dx,dy,obstacles)

   