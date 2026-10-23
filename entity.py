import pygame


class Entity:
    def __init__(self, x, y, health, damage, speed):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.rect = pygame.Rect(self.x,self.y, 40, 40)

    def move(self, dx, dy, walls):
            #Moves the entity depending on the direction multiplier
            self.x += dx * self.speed
            self.rect.x = self.x

            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0:
                        self.rect.right = wall.rect.left
                    elif dx < 0:
                        self.rect.left = wall.rect.right
                    self.x = self.rect.x
                    
            self.y += dy * self.speed
            self.rect.y = int(self.y)

            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    elif dy < 0:
                        self.rect.top = wall.rect.bottom
                    self.y = self.rect.y

    def loseHealth(self, damage_recieved):
        health -= damage_recieved
    