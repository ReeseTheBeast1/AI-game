import settings
import pygame
import wall

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target):
        self.x = target.rect.x - settings.SCREEN_WIDTH // 2
        self.y = target.rect.y - settings.SCREEN_HEIGHT // 2

        self.x = max(0, min(self.x, settings.WORLD_WIDTH - settings.SCREEN_WIDTH))
        self.y = max(0, min(self.y, settings.WORLD_HEIGHT - settings.SCREEN_HEIGHT))

    def apply(self, entity_rect):
        return entity_rect.move(-self.x, -self.y)