import pygame
from entity import Entity


class Player(Entity):
    def __init__(self, x, y, health=100, damage=20, speed=5):
        super().__init__(x, y, health, damage, speed)

        self.rect = pygame.Rect(self.x,self.y, 40, 40)
    def move(self, dx, dy):
        #Moves the player depending on the direction multiplier
        self.x += dx * self.speed
        self.y+= dy * self.speed

        self.rect.x = self.x
        self.rect.y = self.y

    def loseHealth(self, damage_recieved):
        health -= damage_recieved

    
        
