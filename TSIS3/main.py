import pygame
import sys
import os
import random
from pygame.locals import *

from racer import Player, Enemy, Coin, PowerUp, Obstacle, RoadObject, LANES
from ui import main_menu, game_over_screen, leaderboard_screen, username_input, settings_screen
from persistence import load_settings, save_score
import constants

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMG_DIR = "C:/Users/ernur/Desktop/myproject/python_base/TSIS3/images_and_sounds"
SND_DIR = IMG_DIR

DIFFICULTY = {
    "easy":   {"speed": 3,  "inc": 0.05},
    "normal": {"speed": 5,  "inc": 0.10},
    "hard":   {"speed": 8,  "inc": 0.18},
}


MAX_OBSTACLES = 1
MAX_COINS     = 2
SPAWN_CHANCE  = 0.02


def get_max_enemies(level):
    return 3 if level >= 50 else 2


def has_free_lane(enemy_group, obstacle_group):
    occupied = set()

    for obj in list(enemy_group) + list(obstacle_group):
        if obj.rect.top > 200:
            for lane in LANES:
                if abs(obj.rect.centerx - lane) < 60:
                    occupied.add(lane)

    return len(occupied) < len(LANES)


def try_spawn(level, enemy_group, obstacle_group, all_sprites, player):
    max_enemies = get_max_enemies(level)
    can_spawn_enemy    = len(enemy_group)    < max_enemies
    can_spawn_obstacle = len(obstacle_group) < MAX_OBSTACLES

    if not (can_spawn_enemy or can_spawn_obstacle):
        return

    if random.random() >= SPAWN_CHANCE:
        return

    if not has_free_lane(enemy_group, obstacle_group):
        return

    if can_spawn_enemy and (not can_spawn_obstacle or random.random() < 0.6):
        enemy = Enemy(player_rect=player.rect)
        enemy_group.add(enemy)
        all_sprites.add(enemy)
    elif can_spawn_obstacle:
        obstacle = Obstacle(player_rect=player.rect)
        obstacle_group.add(obstacle)
        all_sprites.add(obstacle)


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

ROAD_EVENT    = USEREVENT + 1
INC_SPEED     = USEREVENT + 2
SPAWN_POWERUP = USEREVENT + 3

pygame.time.set_timer(ROAD_EVENT,    15000)
pygame.time.set_timer(INC_SPEED,      1000)
pygame.time.set_timer(SPAWN_POWERUP,  7000)


def run_game(settings):
    RoadObject.clear_registry()

    difficulty = DIFFICULTY[settings.get("difficulty", "normal")]
    constants.SPEED = difficulty["speed"]

    bg = pygame.image.load(os.path.join("C:/Users/ernur/Desktop/myproject/python_base/TSIS3/images_and_sounds/Road.png")).convert()
    bg_y = 0

    # Music
    music_path = os.path.join(SND_DIR, "background.mp3")
    if settings.get("sound") and os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


    player = Player(car_color=settings.get("car_color", "yellow"))

    all_sprites    = pygame.sprite.Group(player)
    enemy_group    = pygame.sprite.Group()
    coin_group     = pygame.sprite.Group()
    powerup_group  = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()

    for kind in ['oncoming', 'traffic']:
        enemy = Enemy(kind=kind, player_rect=player.rect)
        enemy_group.add(enemy)
        all_sprites.add(enemy)

    obstacle = Obstacle(player_rect=player.rect)
    obstacle_group.add(obstacle)
    all_sprites.add(obstacle)

    for _ in range(2):
        coin = Coin(player.rect)
        coin_group.add(coin)
        all_sprites.add(coin)

    score = 0
    coins = 0
    distance = 0

    font = pygame.font.SysFont("Verdana", 16)
    font_bold = pygame.font.SysFont("Verdana", 14, bold=True)

    running = True

    while running:
        dt = clock.tick(constants.FPS) / 1000
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == INC_SPEED:
                constants.SPEED += difficulty["inc"]

            elif event.type == SPAWN_POWERUP:
                if len(powerup_group) == 0:
                    powerup = PowerUp(player_rect=player.rect)
                    powerup_group.add(powerup)
                    all_sprites.add(powerup)

            elif event.type == ROAD_EVENT:
                blocked_lane = random.choice(LANES)
                for i in range(3):
                    if random.random() < 0.5:
                        obstacle = Obstacle(
                            player_rect=player.rect,
                            lane=blocked_lane,
                            offset_y=-60 - i * 120
                        )
                        obstacle_group.add(obstacle)
                        all_sprites.add(obstacle)

        player.update_timers(dt)
        player.move()

        for group in [enemy_group, coin_group, obstacle_group]:
            for obj in group:
                obj.move()

        for pu in list(powerup_group):
            pu.move(dt)

        distance += int(constants.SPEED)
        score += int(constants.SPEED * 0.1)

        level = coins * 2 + (distance // 100)
        try_spawn(level, enemy_group, obstacle_group, all_sprites, player)

        # Collisions 
        for coin in pygame.sprite.spritecollide(player, coin_group, False):
            coins += coin.value
            score += coin.value * 10
            coin._spawn(player.rect)

        for pu in pygame.sprite.spritecollide(player, powerup_group, True):
            player.apply_powerup(pu.kind)

        if pygame.sprite.spritecollideany(player, enemy_group):
            if player.take_hit():
                running = False

        for obs in pygame.sprite.spritecollide(player, obstacle_group, False):
            if player.take_hit():
                running = False
            obs._spawn(player.rect)


        bg_y = (bg_y + int(constants.SPEED)) % constants.SCREEN_HEIGHT

        screen.blit(bg, (0, bg_y - constants.SCREEN_HEIGHT))
        screen.blit(bg, (0, bg_y))


        for spr in all_sprites:
            rect = getattr(spr, 'draw_rect', spr.rect)
            screen.blit(spr.image, rect)

        for i in range(player.lives):
            pygame.draw.circle(screen, (255, 60, 60), (15 + i * 22, 15), 8)

        hud_lines = [
            f"Score: {score}",
            f"Coins: {coins}",
            f"Dist: {distance // 100} m",
        ]

        for i, line in enumerate(hud_lines):
            screen.blit(font.render(line, True, (255, 255, 255)), (10, 30 + i * 20))

        if player.nitro_active:
            screen.blit(font_bold.render(f"NITRO {player.nitro_timer:.1f}s", True, (255, 220, 0)),
                        (constants.SCREEN_WIDTH - 130, 10))

        if player.shield_active:
            screen.blit(font_bold.render("SHIELD", True, (0, 200, 255)),
                        (constants.SCREEN_WIDTH - 130, 30))

        pygame.display.flip()

    pygame.mixer.music.stop()



    crash_path = os.path.join("C:/Users/ernur/Desktop/myproject/python_base/TSIS3/images_and_sounds/crash.wav")
    if settings.get("sound") and os.path.exists(crash_path):
        pygame.mixer.Sound(crash_path).play()

    return score, distance // 100, coins


def main():
    settings = load_settings()

    while True:
        action = main_menu(screen)

        if action == 'quit':
            pygame.quit()
            sys.exit()

        elif action == 'settings':
            settings = settings_screen(screen)

        elif action == 'leaderboard':
            leaderboard_screen(screen)

        elif action == 'play':
            name = username_input(screen)

            while True:
                score, distance, coins = run_game(settings)
                choice = game_over_screen(screen, score, distance, coins)

                if choice != 'retry':
                    break

            save_score(name, score, distance, coins)


if __name__ == "__main__":
    main()