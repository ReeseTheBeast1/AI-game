import pygame
from entity import Entity


class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, damage=15, speed=3, color=(255,0,0))

    def chase(self, player, walls):
        dx = 0
        dy = 0

        if self.x < player.x:
            dx = 1
        elif self.x > player.x:
            dx = -1

        if self.y < player.y:
            dy = 1
        elif self.y > player.y:
            dy = -1

        self.move(dx,dy, walls)



    
        
