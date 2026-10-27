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
     max_height = settings.ROOM_HEIGHT_MIN
    
     for room_index in range(settings.NUM_ROOMS):
        room_width = random.randint(settings.ROOM_WIDTH_MIN, settings.ROOM_WIDTH_MAX)
        room_width = room_width - (room_width % 10)

        room_height = random.randint(settings.ROOM_HEIGHT_MIN, settings.ROOM_HEIGHT_MAX)
        room_height = room_height - (room_height % 10)

        if room_height > max_height:
            max_height = room_height

        #First we calculate the base X offset 
        room_start_x =  current_x

        walls.append(Wall(room_start_x, 0, room_width, 20))
        walls.append(Wall(room_start_x, room_height - 20, room_width, 20))

        door_height = 140
        door_top = (room_height //2) - (door_height // 2)
        door_bottom = (room_height // 2) + (door_height // 2)

        if room_index > 0:
            walls.append(Wall(room_start_x, 0, 20, door_top))
            walls.append(Wall(room_start_x, door_bottom, 20, room_height - door_bottom))
        else:
            walls.append(Wall(room_start_x, 0, 20, room_height))

        if room_index < settings.NUM_ROOMS - 1:
            walls.append(Wall(room_start_x + room_width - 20, 0, 20, door_top))     # Top-right post
            walls.append(Wall(room_start_x + room_width - 20, door_bottom, 20, room_height - door_bottom))   # Bottom-right post
        else:
            walls.append(Wall(room_start_x + room_width - 20, 0, 20, room_height))

        layout_choice = random.choice(["pillars","barriers","empty"])

        if layout_choice == "pillars":
            pillar_w = 40
            pillar_h = room_height // 2
            pillar_y = room_height // 4
            # Add two pillars inside the room
            walls.append(Wall(room_start_x + room_width // 3, pillar_y, pillar_w, pillar_h))
            walls.append(Wall(room_start_x + (room_width // 3) *  2, pillar_y, pillar_w, pillar_h))
            
        elif layout_choice == "barriers":
            barrier_w = room_width // 3
            # Add horizontal barricades forcing up/down movement
            walls.append(Wall(room_start_x + room_width // 3, room_height // 4 - 20, barrier_w, 30))
            walls.append(Wall(room_start_x + room_width // 3, (room_height // 4) * 3, barrier_w, 30))

        current_x += room_width

     settings.WORLD_WIDTH = current_x
     settings.WORLD_HEIGHT = max_height

     return walls