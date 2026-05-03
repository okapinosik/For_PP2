import random
import pygame

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'RIGHT'
    
    def move(self, grow=False):
        head_x, head_y = self.body[0]
        if self.direction == 'RIGHT':
            new_head = (head_x + 20, head_y)
        elif self.direction == 'LEFT':
            new_head = (head_x - 20, head_y)
        elif self.direction == 'UP':
            new_head = (head_x, head_y - 20)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 20)
        
        new_head = (new_head[0] % 600, new_head[1] % 600)
            
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()
            
    def change_direction(self, new_direction):
        opposite = {'RIGHT': 'LEFT', 'LEFT': 'RIGHT', 'UP': 'DOWN', 'DOWN': 'UP'}
        if new_direction != opposite[self.direction]:
            self.direction = new_direction
    
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.weight = 1
        self.is_poison = False      
        self.spawn_time = 0        
        self.lifetime = 5000       
        self.respawn([])           

    def respawn(self, snake_body, obstacles=[]):
        while True:
            new_pos = (random.randrange(0, 600, 20), random.randrange(0, 600, 20))
            if new_pos not in snake_body:
                self.position = new_pos
                break
        
        # Шанс 20% на яд
        self.is_poison = random.random() < 0.2
        self.weight = 0 if self.is_poison else random.randint(1, 3)
        self.spawn_time = pygame.time.get_ticks()
        
    def is_expired(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.lifetime
  

class PowerUp:
    def __init__(self):
        self.position = None
        self.type = None 
        self.spawn_time = 0
        self.lifetime = 8000  
        self.active = False

    def spawn(self, snake_body, food_pos, obstacles=[]):
        while True:
            new_pos = (random.randrange(0, 600, 20), random.randrange(0, 600, 20))
            if new_pos not in snake_body and new_pos != food_pos:
                self.position = new_pos
                break
        
        self.type = random.choice(['speed', 'slow', 'shield'])
        self.spawn_time = pygame.time.get_ticks()
        self.active = True

    def is_expired(self):
        if not self.active: return False
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    
class Obstacles:
    def __init__(self):
        self.blocks = []

    def generate(self, level, snake_body):
        self.blocks = []
        if level < 3: return 
        num_blocks = level + 2 
        
        while len(self.blocks) < num_blocks:
            x = random.randrange(0, 600, 20)
            y = random.randrange(0, 600, 20)
            pos = (x, y)
            head_x, head_y = snake_body[0]
            distance = abs(x - head_x) + abs(y - head_y)
            
            if pos not in snake_body and distance > 60:
                self.blocks.append(pos)