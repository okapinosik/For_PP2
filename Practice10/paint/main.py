import pygame

pygame.init()

def draw_circle(screen, color, pos):
    pygame.draw.circle(screen, color, pos, 10)

def draw_rectangle(screen, color, pos):
    pygame.draw.rect(screen, color, (pos[0] - 10, pos[1] - 10, 20, 20))

def erase(screen, pos):
    pygame.draw.circle(screen, (255, 255, 255), pos, 20)
    
def main():
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    
    screen.fill((255, 255, 255))
    
    color = (0, 0, 255)
    mode = 'circle'
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    mode = 'circle'
                if event.key == pygame.K_r:
                    mode = 'rectangle'
                if event.key == pygame.K_e:
                    mode = 'erase'
                
                if event.key == pygame.K_1:
                    color = (0, 0, 255)
                if event.key == pygame.K_2:
                    color = (0, 255, 0)
                if event.key == pygame.K_3:
                    color = (255, 0, 0)
                    
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            pos = pygame.mouse.get_pos()
            if mode == 'circle':
                draw_circle(screen, color, pos)
            elif mode == 'rectangle':
                draw_rectangle(screen, color, pos)
            elif mode == 'erase':
                erase(screen, pos)
            
        pygame.display.flip()
        clock.tick(165)                    
                    
if __name__ == "__main__":
    main()