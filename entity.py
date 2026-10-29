import pygame
import settings

class Entity:
    def __init__(self, x, y, health, damage, speed, gravity, is_grounded, y_velocity, color=(255,255,255)):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.gravity = gravity
        self.color = color
        self.y_velocity = y_velocity
        self.is_grounded = is_grounded
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

            # self.y += dy * self.speed
            if dy != 0 and self.is_grounded:
                self.y_velocity = 15 * dy
                self.is_grounded = False
                
            
            self.y += self.y_velocity
            self.rect.y = self.y
            self.y_velocity += self.gravity

            if self.rect.bottom >= (settings.WORLD_HEIGHT - 20):
                self.rect.bottom = settings.WORLD_HEIGHT - 20
                self.is_grounded = True
                self.y_velocity = 0           
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dy > 0:
                        self.rect.bottom = wall.rect.top
                    elif dy < 0:
                        self.rect.top = wall.rect.bottom
                    self.y = self.rect.y

    def loseHealth(self, damage_recieved):
        health -= damage_recieved
