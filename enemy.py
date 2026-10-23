import pygame
from entity import Entity


class Enemy(Entity):
    def __init__(self, x, y, health=100, damage=20, speed=5):
        super().__init__(x, y, health, damage, speed)

        self.rect = pygame.Rect(self.x,self.y, 40, 40)

    
        
