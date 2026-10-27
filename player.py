import pygame
from entity import Entity


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, health=100, damage=15, speed=5, color=(0,128,255))

    
        
