import json
import os
import random
from dataclasses import dataclass

import pygame

import db
from config import WIDTH, HEIGHT, CELL, FPS_BASE, COLORS, DEFAULT_SETTINGS

SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = DEFAULT_SETTINGS.copy()
        result.update(data)
        return result
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


@dataclass
class Button:
    rect: pygame.Rect
    text: str

    def draw(self, surface, font, mouse_pos):
        color = COLORS["button_hover"] if self.rect.collidepoint(mouse_pos) else COLORS["button"]
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        label = font.render(self.text, True, COLORS["text"])
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake PostgreSQL Edition")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 24)
        self.big_font = pygame.font.SysFont("arial", 46, bold=True)
        self.small_font = pygame.font.SysFont("arial", 18)

        self.settings = load_settings()
        self.username = ""
        self.screen_name = "username"
        self.running = True
        self.db_ok = True

        try:
            db.init_db()
        except Exception as exc:
            self.db_ok = False
            print("Database error:", exc)

        self.reset_game()

    # ---------- common UI ----------

    def draw_text(self, text, font, color, x, y, center=False):
        img = font.render(str(text), True, color)
        rect = img.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(img, rect)
        return rect

    def draw_grid(self):
        if not self.settings.get("grid", True):
            return
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, (35, 35, 45), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, (35, 35, 45), (0, y), (WIDTH, y))

    def all_cells(self):
        return [(x, y) for x in range(0, WIDTH, CELL) for y in range(60, HEIGHT, CELL)]

    def random_free_cell(self):
        occupied = set(self.snake) | set(self.obstacles)
        occupied |= {self.food, self.poison}
        if self.power_up:
            occupied.add(self.power_up["pos"])

        free = [cell for cell in self.all_cells() if cell not in occupied]
        return random.choice(free) if free else None

    # ---------- game state ----------

    def reset_game(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - CELL, HEIGHT // 2), (WIDTH // 2 - 2 * CELL, HEIGHT // 2)]
        self.direction = (CELL, 0)
        self.next_direction = (CELL, 0)

        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.speed = FPS_BASE

        self.obstacles = []
        self.food = None
        self.food_value = 1
        self.food_spawn_time = 0
        self.food_lifetime = 9000

        self.poison = None
        self.power_up = None
        self.power_spawn_time = 0
        self.active_power = None
        self.active_power_end = 0
        self.shield = False

        self.result_saved = False
        self.personal_best = 0

        if self.username and self.db_ok:
            try:
                self.personal_best = db.get_personal_best(self.username)
            except Exception as exc:
                self.db_ok = False
                print("Personal best error:", exc)

        self.spawn_food()
        self.spawn_poison()

    def spawn_food(self):
        self.food = self.random_free_cell()
        self.food_value = random.choice([1, 1, 1, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison(self):
        self.poison = self.random_free_cell()

    def spawn_power_up(self):
        if self.power_up is not None:
            return

        pos = self.random_free_cell()
        if pos is None:
            return

        self.power_up = {
            "pos": pos,
            "type": random.choice(["speed", "slow", "shield"]),
            "created": pygame.time.get_ticks(),
        }

    def generate_obstacles(self):
        if self.level < 3:
            self.obstacles = []
            return

        count = min(5 + self.level * 2, 35)
        obstacles = set()
        snake_head = self.snake[0]

        attempts = 0
        while len(obstacles) < count and attempts < 1000:
            attempts += 1
            cell = random.choice(self.all_cells())
            if cell in self.snake or cell == self.food or cell == self.poison:
                continue

            # Простая защита: не ставим стены рядом с головой змейки.
            if abs(cell[0] - snake_head[0]) <= CELL and abs(cell[1] - snake_head[1]) <= CELL:
                continue

            obstacles.add(cell)

        self.obstacles = list(obstacles)

    def change_level_if_needed(self):
        new_level = self.food_eaten // 5 + 1
        if new_level != self.level:
            self.level = new_level
            self.speed = FPS_BASE + self.level
            self.generate_obstacles()

    # ---------- gameplay ----------

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.screen_name = "menu"
                elif event.key in (pygame.K_UP, pygame.K_w) and self.direction != (0, CELL):
                    self.next_direction = (0, -CELL)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and self.direction != (0, -CELL):
                    self.next_direction = (0, CELL)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and self.direction != (CELL, 0):
                    self.next_direction = (-CELL, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != (-CELL, 0):
                    self.next_direction = (CELL, 0)

    def use_shield_or_die(self):
        if self.shield:
            self.shield = False
            return False
        return True

    def update_game(self):
        now = pygame.time.get_ticks()

        # disappearing food
        if now - self.food_spawn_time > self.food_lifetime:
            self.spawn_food()

        # power-up spawn / disappear
        if self.power_up is None and random.random() < 0.006:
            self.spawn_power_up()
        if self.power_up and now - self.power_up["created"] > 8000:
            self.power_up = None

        # active power duration
        if self.active_power and now > self.active_power_end:
            if self.active_power in ("speed", "slow"):
                self.speed = FPS_BASE + self.level
            self.active_power = None

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        hit_border = new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 60 or new_head[1] >= HEIGHT
        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_border or hit_self or hit_obstacle:
            if self.use_shield_or_die():
                self.screen_name = "game_over"
                self.save_game_result()
                return
            # shield спасает: змейка просто не двигается в опасную клетку
            return

        self.snake.insert(0, new_head)
        ate_something = False

        if new_head == self.food:
            self.score += self.food_value
            self.food_eaten += 1
            ate_something = True
            self.change_level_if_needed()
            self.spawn_food()

            if random.random() < 0.35:
                self.spawn_poison()

        if self.poison and new_head == self.poison:
            # poison: минус 2 сегмента
            self.score = max(0, self.score - 1)
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()

            self.poison = None
            self.spawn_poison()

            if len(self.snake) <= 1:
                self.screen_name = "game_over"
                self.save_game_result()
                return

        if self.power_up and new_head == self.power_up["pos"]:
            ptype = self.power_up["type"]
            self.power_up = None

            if ptype == "speed":
                self.active_power = "speed"
                self.speed = FPS_BASE + self.level + 6
                self.active_power_end = now + 5000
            elif ptype == "slow":
                self.active_power = "slow"
                self.speed = max(4, FPS_BASE + self.level - 4)
                self.active_power_end = now + 5000
            elif ptype == "shield":
                self.active_power = "shield"
                self.shield = True

        if not ate_something:
            self.snake.pop()

    def save_game_result(self):
        if self.result_saved:
            return

        self.result_saved = True
        if self.db_ok:
            try:
                db.save_result(self.username or "Player", self.score, self.level)
                self.personal_best = max(self.personal_best, self.score)
            except Exception as exc:
                self.db_ok = False
                print("Save result error:", exc)

    def draw_game(self):
        self.screen.fill(COLORS["bg"])
        self.draw_grid()

        pygame.draw.rect(self.screen, COLORS["panel"], (0, 0, WIDTH, 60))
        self.draw_text(f"Player: {self.username or 'Player'}", self.small_font, COLORS["text"], 12, 8)
        self.draw_text(f"Score: {self.score}", self.small_font, COLORS["text"], 12, 32)
        self.draw_text(f"Level: {self.level}", self.small_font, COLORS["text"], 145, 32)
        self.draw_text(f"Best: {self.personal_best}", self.small_font, COLORS["text"], 260, 32)
        self.draw_text(f"DB: {'OK' if self.db_ok else 'OFF'}", self.small_font, COLORS["muted"], 700, 20)

        if self.shield:
            self.draw_text("SHIELD", self.small_font, COLORS["power_shield"], 570, 20)
        elif self.active_power:
            self.draw_text(self.active_power.upper(), self.small_font, COLORS["bonus_food"], 570, 20)

        for block in self.obstacles:
            pygame.draw.rect(self.screen, COLORS["wall"], (*block, CELL, CELL))

        if self.food:
            color = COLORS["bonus_food"] if self.food_value > 1 else COLORS["food"]
            pygame.draw.rect(self.screen, color, (*self.food, CELL, CELL), border_radius=5)
            if self.food_value > 1:
                self.draw_text(str(self.food_value), self.small_font, COLORS["bg"], self.food[0] + 5, self.food[1] + 1)

        if self.poison:
            pygame.draw.rect(self.screen, COLORS["poison"], (*self.poison, CELL, CELL), border_radius=5)

        if self.power_up:
            ptype = self.power_up["type"]
            pcolor = COLORS[f"power_{ptype}"]
            pygame.draw.circle(self.screen, pcolor, (self.power_up["pos"][0] + CELL // 2, self.power_up["pos"][1] + CELL // 2), CELL // 2)

        snake_color = tuple(self.settings.get("snake_color", DEFAULT_SETTINGS["snake_color"]))
        for i, segment in enumerate(self.snake):
            color = (min(snake_color[0] + 35, 255), min(snake_color[1] + 35, 255), min(snake_color[2] + 35, 255)) if i == 0 else snake_color
            pygame.draw.rect(self.screen, color, (*segment, CELL, CELL), border_radius=6)

    # ---------- screens ----------

    def username_screen(self):
        self.screen.fill(COLORS["bg"])
        self.draw_text("Enter username", self.big_font, COLORS["text"], WIDTH // 2, 170, center=True)
        self.draw_text("Type name and press Enter", self.font, COLORS["muted"], WIDTH // 2, 225, center=True)

        box = pygame.Rect(250, 280, 300, 50)
        pygame.draw.rect(self.screen, COLORS["panel"], box, border_radius=10)
        pygame.draw.rect(self.screen, COLORS["button_hover"], box, 2, border_radius=10)
        self.draw_text(self.username + "|", self.font, COLORS["text"], box.x + 15, box.y + 12)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username.strip():
                    self.username = self.username.strip()[:50]
                    self.reset_game()
                    self.screen_name = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif len(self.username) < 50 and event.unicode.isprintable():
                    self.username += event.unicode

    def menu_screen(self):
        self.screen.fill(COLORS["bg"])
        self.draw_text("SNAKE", self.big_font, COLORS["text"], WIDTH // 2, 120, center=True)
        self.draw_text(f"Hello, {self.username}", self.font, COLORS["muted"], WIDTH // 2, 175, center=True)

        buttons = [
            Button(pygame.Rect(300, 230, 200, 48), "Play"),
            Button(pygame.Rect(300, 295, 200, 48), "Leaderboard"),
            Button(pygame.Rect(300, 360, 200, 48), "Settings"),
            Button(pygame.Rect(300, 425, 200, 48), "Quit"),
        ]

        mouse = pygame.mouse.get_pos()
        for b in buttons:
            b.draw(self.screen, self.font, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for b in buttons:
                if b.clicked(event):
                    if b.text == "Play":
                        self.reset_game()
                        self.screen_name = "game"
                    elif b.text == "Leaderboard":
                        self.screen_name = "leaderboard"
                    elif b.text == "Settings":
                        self.screen_name = "settings"
                    elif b.text == "Quit":
                        self.running = False

    def game_over_screen(self):
        self.screen.fill(COLORS["bg"])
        self.draw_text("GAME OVER", self.big_font, COLORS["text"], WIDTH // 2, 120, center=True)
        self.draw_text(f"Score: {self.score}", self.font, COLORS["text"], WIDTH // 2, 205, center=True)
        self.draw_text(f"Level reached: {self.level}", self.font, COLORS["text"], WIDTH // 2, 245, center=True)
        self.draw_text(f"Personal best: {max(self.personal_best, self.score)}", self.font, COLORS["text"], WIDTH // 2, 285, center=True)

        buttons = [
            Button(pygame.Rect(290, 350, 220, 50), "Retry"),
            Button(pygame.Rect(290, 420, 220, 50), "Main Menu"),
        ]

        mouse = pygame.mouse.get_pos()
        for b in buttons:
            b.draw(self.screen, self.font, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for b in buttons:
                if b.clicked(event):
                    if b.text == "Retry":
                        self.reset_game()
                        self.screen_name = "game"
                    elif b.text == "Main Menu":
                        self.screen_name = "menu"

    def leaderboard_screen(self):
        self.screen.fill(COLORS["bg"])
        self.draw_text("Leaderboard TOP 10", self.big_font, COLORS["text"], WIDTH // 2, 55, center=True)

        rows = []
        if self.db_ok:
            try:
                rows = db.get_top_scores(10)
            except Exception as exc:
                self.db_ok = False
                print("Leaderboard error:", exc)

        headers = ["#", "Username", "Score", "Level", "Date"]
        xs = [60, 120, 360, 470, 570]
        y = 125

        for x, h in zip(xs, headers):
            self.draw_text(h, self.small_font, COLORS["bonus_food"], x, y)

        y += 35
        if not self.db_ok:
            self.draw_text("Database is not connected. Check config.py and PostgreSQL.", self.font, COLORS["muted"], 80, y)
        elif not rows:
            self.draw_text("No results yet.", self.font, COLORS["muted"], 80, y)
        else:
            for i, row in enumerate(rows, start=1):
                self.draw_text(i, self.small_font, COLORS["text"], xs[0], y)
                self.draw_text(row["username"], self.small_font, COLORS["text"], xs[1], y)
                self.draw_text(row["score"], self.small_font, COLORS["text"], xs[2], y)
                self.draw_text(row["level_reached"], self.small_font, COLORS["text"], xs[3], y)
                self.draw_text(row["played_at"], self.small_font, COLORS["text"], xs[4], y)
                y += 30

        back = Button(pygame.Rect(300, 520, 200, 45), "Back")
        mouse = pygame.mouse.get_pos()
        back.draw(self.screen, self.font, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if back.clicked(event):
                self.screen_name = "menu"

    def settings_screen(self):
        self.screen.fill(COLORS["bg"])
        self.draw_text("Settings", self.big_font, COLORS["text"], WIDTH // 2, 75, center=True)

        buttons = [
            Button(pygame.Rect(250, 160, 300, 45), f"Grid: {'ON' if self.settings['grid'] else 'OFF'}"),
            Button(pygame.Rect(250, 225, 300, 45), f"Sound: {'ON' if self.settings['sound'] else 'OFF'}"),
            Button(pygame.Rect(250, 290, 300, 45), "Change Snake Color"),
            Button(pygame.Rect(250, 420, 300, 45), "Save & Back"),
        ]

        self.draw_text("Color presets: green -> blue -> yellow -> pink", self.small_font, COLORS["muted"], WIDTH // 2, 360, center=True)

        mouse = pygame.mouse.get_pos()
        for b in buttons:
            b.draw(self.screen, self.font, mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            for b in buttons:
                if b.clicked(event):
                    if b.text.startswith("Grid"):
                        self.settings["grid"] = not self.settings["grid"]
                    elif b.text.startswith("Sound"):
                        self.settings["sound"] = not self.settings["sound"]
                    elif b.text == "Change Snake Color":
                        presets = [[0, 220, 80], [80, 170, 255], [240, 210, 70], [230, 80, 170]]
                        current = self.settings["snake_color"]
                        idx = presets.index(current) if current in presets else 0
                        self.settings["snake_color"] = presets[(idx + 1) % len(presets)]
                    elif b.text == "Save & Back":
                        save_settings(self.settings)
                        self.screen_name = "menu"

    # ---------- main loop ----------

    def run(self):
        while self.running:
            if self.screen_name == "username":
                self.username_screen()
                self.clock.tick(30)
            elif self.screen_name == "menu":
                self.menu_screen()
                self.clock.tick(30)
            elif self.screen_name == "game":
                self.handle_game_events()
                self.update_game()
                self.draw_game()
                self.clock.tick(self.speed)
            elif self.screen_name == "game_over":
                self.game_over_screen()
                self.clock.tick(30)
            elif self.screen_name == "leaderboard":
                self.leaderboard_screen()
                self.clock.tick(30)
            elif self.screen_name == "settings":
                self.settings_screen()
                self.clock.tick(30)

            pygame.display.flip()

        pygame.quit()
