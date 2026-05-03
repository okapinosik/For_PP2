import pygame
from pygame.locals import *
from scenes import Title, Playing
import sprites
import sys
from code import DBManager
import json
import os

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.defaults = {
            "snake_color": [34, 139, 34],
            "grid_overlay": True,
            "sound": True
        }
        self.data = self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return self.defaults.copy()

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

class Game:
    def __init__(self):
        self.db = DBManager() 
        self.current_username = "Guest"
        self.last_score = 0
        self.snake = sprites.Snake()
        self.food = sprites.Food()
        self.state = Title(self)
        self.settings = SettingsManager()
        pygame.mixer.init() 

        self.eat_sound = pygame.mixer.Sound("C:/Users/ernur/Desktop/myproject/python_base/TSIS4/sounds/eat.mp3")
        self.poison_sound = pygame.mixer.Sound("C:/Users/ernur/Desktop/myproject/python_base/TSIS4/sounds/poison.wav")
        self.powerup_sound = pygame.mixer.Sound("C:/Users/ernur/Desktop/myproject/python_base/TSIS4/sounds/powerup.wav")
        self.death_sound = pygame.mixer.Sound("C:/Users/ernur/Desktop/myproject/python_base/TSIS4/sounds/d.mp3")


def main():
    pygame.init()
    pygame.mixer.init() 
    pygame.display.set_caption('Snake Game')

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        events = pygame.event.get()
        
        for event in events:
            if event.type == QUIT:
                game.settings.save() 
                pygame.quit()
                sys.exit()
        
        game.state.handle_events(events)
        game.state.update()
        game.state.draw(SCREEN)
        pygame.display.update()
        
        if isinstance(game.state, Playing):
            clock.tick(game.state.current_speed())
        else:
            clock.tick(30)

if __name__ == '__main__':
    main()