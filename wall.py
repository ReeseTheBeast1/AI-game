import pygame
import settings
import random

class Wall:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.rect = pygame.Rect(self.x,self.y, self.height, self.width)
    
def generate_linear_dungeon():
     walls = []
     current_x = 0
     max_height = settings.ROOM_HEIGHT_MAX
     
    
     for room_index in range(settings.NUM_ROOMS):
        room_width = random.randint(settings.ROOM_WIDTH_MIN, settings.ROOM_WIDTH_MAX)
        room_width = room_width - (room_width % 10)

        room_height = random.randint(settings.ROOM_HEIGHT_MAX, settings.ROOM_HEIGHT_MIN)
        room_height = room_height - (room_height % 10)

        if settings.WORLD_HEIGHT - room_height < max_height:
            max_height = room_height

        #First we calculate the base X offset 
        room_start_x =  current_x
        floor = settings.WORLD_HEIGHT - 20
        ceiling = floor - room_height
        walls.append(Wall(room_start_x, floor, room_width, 20)) #floor
        walls.append(Wall(room_start_x, floor - room_height, room_width, 20)) #ceiling

        door_height = 80
        door_top = room_height - door_height

        #left walls
        if room_index > 0:
            walls.append(Wall(room_start_x, ceiling, 20, door_top))
        else:
            walls.append(Wall(room_start_x, ceiling, 20, floor))

        #right walls
        if room_index < settings.NUM_ROOMS - 1:
            walls.append(Wall(room_start_x + room_width - 20, ceiling, 20, door_top))    
        else:
            walls.append(Wall(room_start_x + room_width - 20, ceiling , 20, floor))

        current_x += room_width

     settings.WORLD_WIDTH = current_x

     return walls