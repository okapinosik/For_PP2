import pygame
from pygame.locals import *
from scenes import Title, Playing
import sprites
import sys

class Game:
    def __init__(self):
        self.snake = sprites.Snake()
        self.food = sprites.Food()
        self.state = Title(self)

def main():
    pygame.init()
    pygame.display.set_caption('Snake Game')

    SCREEN = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    game = Game()
    
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
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