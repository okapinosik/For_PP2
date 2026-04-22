import random

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
        
        self.respawn([])
        
    def respawn(self, snake_body):
        while True:
            new_pos = (random.randrange(0, 600, 20), random.randrange(0, 600, 20))
            
            if new_pos not in snake_body:
                self.position = new_pos
                break