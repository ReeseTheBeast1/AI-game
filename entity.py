import pygame


class Entity:
    def __init__(self, x, y, health, damage, speed):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed

        self.rect = pygame.Rect(self.x,self.y, 40, 40)

    def wall_collision(self, wall):
        if self.y > 0:
            self.rect.bottom= wall.top
        if self.y < 0:
            self.rect.top = wall.bottom
        if self.x > 0:
            self.rect.bottom= wall.left
        if self.x < 0:
            self.rect.top = wall.right
         


    def loseHealth(self, damage_recieved):
        health -= damage_recieved
    