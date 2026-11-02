import pygame
import settings

class Entity:
    def __init__(self, x, y, health, damage, speed, gravity, direction, attack_range, attack_cooldown, is_grounded, y_velocity, color=(255,255,255)):
        self.x = x
        self.y = y
        self.health = health
        self.damage = damage
        self.speed = speed
        self.gravity = gravity
        self.color = color
        self.y_velocity = y_velocity
        self.is_grounded = is_grounded
        self.direction = direction
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.last_attack_time = 0
        self.rect = pygame.Rect(self.x,self.y, 40, 40)

    def get_vision_rect(self, distance):
        if self.direction == "RIGHT":
            return pygame.Rect(self.rect.right, self.rect.y, distance, self.rect.height)
        elif self.direction == "LEFT":
            return pygame.Rect(self.rect.left - distance, self.rect.y, distance, self.rect.height)
        return pygame.Rect(0, 0, 0, 0)
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
            for wall in walls:
                if self.rect.colliderect(wall.rect):    
                    if self.y_velocity > 0:
                        self.rect.bottom = wall.rect.top
                        self.is_grounded = True
                        self.y_velocity = 0
                    elif self.y_velocity < 0:
                        self.rect.top = wall.rect.bottom
                        self.y_velocity = 0
                    self.y = self.rect.y

    def check_enemies_in_front(self, entity_list, distance):
        """Returns a list of all enemies currently in front of the player within distance."""
        entity_spotted = []
        vision_rect = self.get_vision_rect(distance)
        # Optional: Use this to visualize the range while debugging
        # pygame.draw.rect(screen, (255, 0, 0), vision_rect, 1)
    
        for entity in entity_list:
            # Check if the enemy's rect collides with the player's vision rect
            if vision_rect.colliderect(entity.rect):
                    entity_spotted.append(entity)
    
            return entity_spotted

    def loseHealth(self, damage_recieved):
        self.health -= damage_recieved

    def execute_strike(self, targets):

        current_time = pygame.time.get_ticks()

        if current_time - self.last_attack_time >= self.attack_cooldown:
            attack_box = self.get_vision_rect(self.attack_range)

            hit_something = False
            for target in targets:
                if attack_box.colliderect(target.rect):
                    target.loseHealth(self.damage)
                    print(f"{type(self).__name__} hit {type(target).__name__}! Target Health: {target.health}")
                    hit_something = True
            self.last_attack_time = current_time



       