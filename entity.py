import pygame


class Entity:
    def __init__(self, x, y, health, damage, speed):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed