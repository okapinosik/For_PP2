import pygame
from pygame.locals import *
import sys
from code import DBManager
import random

class Title:
    def __init__(self, game):
        self.game = game
        self.username = ""
        self.font = pygame.font.SysFont('Arial', 40)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(self.username) > 0:
                        self.game.current_username = self.username
                        import scenes
                        self.game.state = scenes.Menu(self.game)
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    if len(self.username) < 15 and event.unicode.isalnum():
                        self.username += event.unicode

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((135, 206, 250))
        title_text = self.font.render('SNAKE GAME', True, (0, 0, 0))
        prompt_text = self.font.render('enter name', True, (0, 0, 0))
        name_text = self.font.render(self.username + "_", True, (0, 0, 0))
        
        screen.blit(title_text, (180, 180))
        screen.blit(prompt_text, (210, 240))
        screen.blit(name_text, (240, 300))

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 40)
        self.small_font = pygame.font.SysFont('Arial', 25)
        self.btn_play = pygame.Rect(200, 150, 200, 50)
        self.btn_leader = pygame.Rect(200, 220, 200, 50)
        self.btn_settings = pygame.Rect(200, 290, 200, 50)
        self.btn_quit = pygame.Rect(200, 360, 200, 50)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.btn_play.collidepoint(event.pos):
                        from scenes import Playing
                        self.game.state = Playing(self.game)
                    elif self.btn_leader.collidepoint(event.pos):
                        from scenes import Leaderboard
                        self.game.state = Leaderboard(self.game)
                    elif self.btn_settings.collidepoint(event.pos):
                        from scenes import SettingsMenu
                        self.game.state = SettingsMenu(self.game)
                    elif self.btn_quit.collidepoint(event.pos):
                        pygame.quit()
                        import sys
                        sys.exit()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((30, 30, 40))
    
        btns = [
            (self.btn_play, "PLAY", (255, 255, 0)),
            (self.btn_leader, "LEADERS", (153, 50, 204)),
            (self.btn_settings, "SETTINGS", (153, 50, 204)),
            (self.btn_quit, "QUIT", (255, 255, 0))
        ]

        for rect, text, color in btns:
            pygame.draw.rect(screen, (40, 40, 55), rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
            txt = self.small_font.render(text, True, (255, 255, 255))
            screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

class Leaderboard:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.SysFont('Arial', 40)
        self.font_text = pygame.font.SysFont('Arial', 22)
        self.top_data = self.game.db.get_top_10() 
        self.btn_back = pygame.Rect(200, 520, 200, 40)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_back.collidepoint(event.pos):
                    from scenes import Menu
                    self.game.state = Menu(self.game)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes import Menu
                    self.game.state = Menu(self.game)

    def update(self): pass

    def draw(self, screen):
        screen.fill((153, 50, 204))
        
        title = self.font_title.render("TOP 10 LEADERS", True, (255, 255, 0))
        screen.blit(title, (600 // 2 - title.get_width() // 2, 30))

        header = self.font_text.render("RANK  NAME      SCORE  LVL   DATE", True, (75, 0, 130))
        screen.blit(header, (50, 100))
        
        for i, row in enumerate(self.top_data):
            try:
                name_val = str(row[0]) if len(row) > 0 else "Unknown"
                score_val = str(row[1]) if len(row) > 1 else "0"
                lvl_val = str(row[2]) if len(row) > 2 else "1"
                date_val = str(row[3]) if len(row) > 3 else "---"

                rank = f"{i+1}."
                name_text = f"{name_val[:10]}" 
                color = (255, 255, 0) if name_val == self.game.current_username else (255, 255, 255)
                
                screen.blit(self.font_text.render(rank, True, color), (50, 140 + i*35))
                screen.blit(self.font_text.render(name_text, True, color), (100, 140 + i*35))
                screen.blit(self.font_text.render(score_val, True, color), (220, 140 + i*35))
                screen.blit(self.font_text.render(lvl_val, True, color), (290, 140 + i*35))
                screen.blit(self.font_text.render(date_val, True, color), (360, 140 + i*35))

            except Exception as e:
                print(f"Error rendering row {i}: {e}")
                continue

        pygame.draw.rect(screen, (40, 40, 55), self.btn_back, border_radius=10)
        back_txt = self.font_text.render("BACK", True, (255, 255, 255))
        screen.blit(back_txt, (self.btn_back.centerx - back_txt.get_width()//2, self.btn_back.centery - back_txt.get_height()//2))

class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 25)
        self.title_font = pygame.font.SysFont('Arial', 40)
        self.colors = [("Green", [152, 251, 152]), ("Blue", [175, 238, 238]), ("Yellow", [255, 255, 0])]
        self.c_idx = 0
        
        current_color = self.game.settings.data.get("snake_color", [152, 251, 152])
        for i, (name, val) in enumerate(self.colors):
            if val == current_color:
                self.c_idx = i
                break
        
        self.btn_color = pygame.Rect(170, 150, 250, 40)
        self.btn_grid = pygame.Rect(170, 210, 250, 40)
        self.btn_sound = pygame.Rect(170, 270, 250, 40)
        self.btn_save = pygame.Rect(170, 380, 250, 50)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes import Menu
                    self.game.state = Menu(self.game)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.btn_color.collidepoint(event.pos):
                        self.c_idx = (self.c_idx + 1) % len(self.colors)
                        self.game.settings.data["snake_color"] = self.colors[self.c_idx][1]
                    
                    elif self.btn_grid.collidepoint(event.pos):
                        self.game.settings.data["grid_overlay"] = not self.game.settings.data.get("grid_overlay", True)
                    
                    elif self.btn_sound.collidepoint(event.pos):
                        self.game.settings.data["sound"] = not self.game.settings.data.get("sound", True)
                    
                    elif self.btn_save.collidepoint(event.pos):
                        self.game.settings.save() 
                        from scenes import Menu
                        self.game.state = Menu(self.game)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((153, 50, 204))
        title = self.title_font.render("SETTINGS", True, (255, 255, 0))
        screen.blit(title, (600 // 2 - title.get_width() // 2, 30))

        grid_status = "ON" if self.game.settings.data.get("grid_overlay", True) else "OFF"
        sound_status = "ON" if self.game.settings.data.get("sound", True) else "OFF"
        color_name = self.colors[self.c_idx][0]

        buttons = [
            (self.btn_color, f"Snake Color: {color_name}"),
            (self.btn_grid, f"Grid Overlay: {grid_status}"),
            (self.btn_sound, f"Sound: {sound_status}"),
        ]

        for rect, text in buttons:
            pygame.draw.rect(screen, (255,255,255), rect, border_radius=5)
            pygame.draw.rect(screen, (75, 0, 130), rect, 2, border_radius=5)
            txt_surf = self.font.render(text, True, (75, 0, 130))
            screen.blit(txt_surf, (rect.x + 10, rect.centery - txt_surf.get_height() // 2))

        pygame.draw.rect(screen, (75, 0, 130), self.btn_save, border_radius=10)
        save_txt = self.font.render("SAVE & BACK", True, (255, 255, 255))
        screen.blit(save_txt, (self.btn_save.centerx - save_txt.get_width() // 2, self.btn_save.centery - save_txt.get_height() // 2))


class Playing:
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.level = 1
        self.personal_best = self.game.db.get_personal_best(self.game.current_username)
        self.death_sound = pygame.mixer.Sound("C:/Users/ernur/Desktop/myproject/python_base/TSIS4/sounds/d.mp3") 
        self.game.snake.__init__()
        self.game.food.respawn(self.game.snake.body) 
        
        import sprites 
        self.powerup = sprites.PowerUp() 
        
        self.active_effect = None       
        self.effect_start_time = 0     
        self.effect_duration = 5000    
        self.has_shield = False        

        self.obstacles = sprites.Obstacles()
        self.obstacles.generate(self.level, self.game.snake.body)

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                #--------------------------------------------
                # УДАЛИТЬ ПОТОМ
                if event.key == K_e:
                    self.game.last_score = self.score
                    self.game.db.save_result(
                        self.game.current_username, 
                        self.score, 
                        self.level
                    )
                    self.game.state = GameOver(self.game)
                # ---------------------------------------

                if event.key == K_UP: self.game.snake.change_direction('UP')
                elif event.key == K_DOWN: self.game.snake.change_direction('DOWN')
                elif event.key == K_LEFT: self.game.snake.change_direction('LEFT')
                elif event.key == K_RIGHT: self.game.snake.change_direction('RIGHT')
        
    def update(self):
        now = pygame.time.get_ticks()
        head = self.game.snake.body[0]
        
        ate_food = (head == self.game.food.position)
        ate_powerup = (self.powerup.active and head == self.powerup.position)

        if ate_food:
            if self.game.food.is_poison:
                if self.game.settings.data.get("sound"):
                    self.game.poison_sound.play() 
                if len(self.game.snake.body) <= 3:
                    self.game.last_score = self.score
                    self.game.db.save_result(self.game.current_username, self.score, self.level)
                    self.game.state = GameOver(self.game)
                    return
                else:
                    self.game.snake.body.pop()
                    self.game.snake.body.pop()
            else:
                if self.game.settings.data.get("sound"):
                    self.game.eat_sound.play()
                self.score += self.game.food.weight
                if self.score // 5 + 1 > self.level:
                    self.level += 1
                    self.obstacles.generate(self.level, self.game.snake.body)
            self.game.food.respawn(self.game.snake.body, self.obstacles.blocks)

        elif self.game.food.is_expired():
            self.game.food.respawn(self.game.snake.body, self.obstacles.blocks)

        if ate_powerup:
            if self.game.settings.data.get("sound"):
                self.game.powerup_sound.play()
            
            if self.powerup.type == 'shield':
                self.has_shield = True
            else:
                self.active_effect = self.powerup.type
                self.effect_start_time = now
            
            self.powerup.active = False
        if not self.powerup.active and random.random() < 0.01:
            self.powerup.spawn(self.game.snake.body, self.game.food.position, self.obstacles.blocks)
            
        if self.powerup.is_expired():
            self.powerup.active = False
            
        if self.active_effect and now - self.effect_start_time > self.effect_duration:
            self.active_effect = None

        is_normal_growth = ate_food and not self.game.food.is_poison
        self.game.snake.move(grow=is_normal_growth)

        
        new_head = self.game.snake.body[0]
        out_of_bounds = new_head[0] < 0 or new_head[0] >= 600 or new_head[1] < 0 or new_head[1] >= 600
        self_collision = new_head in self.game.snake.body[1:]
        hit_obstacle = new_head in self.obstacles.blocks
        
        if out_of_bounds or self_collision or hit_obstacle:
            if self.has_shield:
                self.has_shield = False
            else:
                if self.game.settings.data.get("sound", True):
                    try:
                        self.game.death_sound.play()
                    except:
                        print("Файл звука не найден или поврежден")

                self.game.last_score = self.score
                self.game.last_level = self.level
                self.game.db.save_result(self.game.current_username, self.score, self.level)
                self.game.state = GameOver(self.game)
        

        out_of_bounds = new_head[0] < 0 or new_head[0] >= 600 or new_head[1] < 0 or new_head[1] >= 600
        self_collision = new_head in self.game.snake.body[1:]
        hit_obstacle = new_head in self.obstacles.blocks
        
        if out_of_bounds or self_collision or hit_obstacle:
            if self.has_shield:
                self.has_shield = False  
            else:
                if self.game.settings.data.get("sound"):
                    self.game.death_sound.play()
                
                self.game.last_score = self.score
                self.game.db.save_result(self.game.current_username, self.score, self.level)
                self.game.last_level = self.level
                self.game.state = GameOver(self.game)
        
                    
    def draw(self, screen):
        screen.fill((135, 206, 250))
        if self.game.settings.data.get("grid_overlay", True):
            for x in range(0, 600, 20):
                pygame.draw.line(screen, (199, 21,133), (x, 0), (x, 600))
            for y in range(0, 600, 20):
                pygame.draw.line(screen, (199, 21,133), (0, y), (600, y))

        for block in self.obstacles.blocks:
            pygame.draw.rect(screen, (199, 21,133), (*block, 20, 20))
            pygame.draw.rect(screen, (199, 21,133), (*block, 20, 20), 2)

        if self.game.food.is_poison:
            food_color = (25, 25, 112)  
        else:
            colors = {1: (165, 42, 42), 2: (255, 255, 0), 3: (238, 130, 238)}
            food_color = colors.get(self.game.food.weight, (255, 0, 0))
        pygame.draw.rect(screen, food_color, (*self.game.food.position, 20, 20))

        if self.powerup.active:
            p_colors = {'speed': (0, 255, 255), 'slow': (255, 165, 0), 'shield': (255, 255, 255)}
            p_color = p_colors.get(self.powerup.type, (255, 255, 255))
            center = (self.powerup.position[0] + 10, self.powerup.position[1] + 10)
            pygame.draw.circle(screen, p_color, center, 10)

        snake_color = self.game.settings.data.get("snake_color", [152, 251, 152])
        for i, segment in enumerate(self.game.snake.body):
            pygame.draw.rect(screen, snake_color, (*segment, 20, 20))
            
            # Если надет ЩИТ, рисуем белую рамку вокруг головы
            if i == 0 and self.has_shield:
                pygame.draw.rect(screen, (255, 255, 255), (segment[0]-2, segment[1]-2, 24, 24), 2)

        font = pygame.font.SysFont('Arial', 20)
        food_status = "POISON" if self.game.food.is_poison else self.game.food.weight
        main_info = (f"Lvl: {self.level} | "
                     f"Weight: {food_status} | "
                     f"Score: {self.score} | "
                     f"Best: {max(self.personal_best, self.score)}")
        
        info_surface = font.render(main_info, True, (255, 255, 255))
        screen.blit(info_surface, (10, 10))

        if self.active_effect:
            eff_color = (0, 255, 255) if self.active_effect == 'speed' else (255, 165, 0)
            eff_surface = font.render(f"EFFECT: {self.active_effect.upper()}", True, eff_color)
            screen.blit(eff_surface, (10, 40))
    
    def current_speed(self):
        base_speed = 10 + (self.level - 1) * 2
        if self.active_effect == 'speed':
            return base_speed + 10
        if self.active_effect == 'slow':
            return max(5, base_speed - 5)
        return base_speed
            
class GameOver:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.SysFont('Arial', 50)
        self.font_stats = pygame.font.SysFont('Arial', 25)
        self.font_btn = pygame.font.SysFont('Arial', 30)
        self.personal_best = self.game.db.get_personal_best(self.game.current_username)
        self.btn_retry = pygame.Rect(100, 450, 180, 50)
        self.btn_menu = pygame.Rect(320, 450, 180, 50)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_retry.collidepoint(event.pos):
                    from scenes import Playing
                    self.game.state = Playing(self.game)
                elif self.btn_menu.collidepoint(event.pos):
                    from scenes import Menu
                    self.game.state = Menu(self.game)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    from scenes import Playing
                    self.game.state = Playing(self.game)
                if event.key == pygame.K_ESCAPE:
                    from scenes import Menu
                    self.game.state = Menu(self.game)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((135, 206, 250)) 
        title_surf = self.font_title.render('GAME OVER', True, (199, 21, 133))
        screen.blit(title_surf, (600 // 2 - title_surf.get_width() // 2, 60))
        stats = [
            f"Player: {self.game.current_username}",
            f"Final Score: {self.game.last_score}",
            f"Level Reached: {getattr(self.game, 'last_level', 1)}"
            f" Personal Best: {self.personal_best}"
        ]

        for i, text in enumerate(stats):
            color = (255, 255, 255)
            if "Score" in text: color = (255, 255, 0) 
            stat_surf = self.font_stats.render(text, True, color)
            screen.blit(stat_surf, (600 // 2 - stat_surf.get_width() // 2, 150 + i * 40))

        pygame.draw.rect(screen, (40, 40, 55), self.btn_retry, border_radius=10)
        retry_txt = self.font_btn.render("Retry", True, (255, 255, 255))
        screen.blit(retry_txt, (self.btn_retry.centerx - retry_txt.get_width() // 2, self.btn_retry.centery - retry_txt.get_height() // 2))


        pygame.draw.rect(screen, (40, 40, 55), self.btn_menu, border_radius=10)
        menu_txt = self.font_btn.render("Menu", True, (255, 255, 255))
        screen.blit(menu_txt, (self.btn_menu.centerx - menu_txt.get_width() // 2, self.btn_menu.centery - menu_txt.get_height() // 2))


        hint = self.font_stats.render("Use mouse or SPACE to restart", True, (255,192, 203))
        screen.blit(hint, (600 // 2 - hint.get_width() // 2, 530))