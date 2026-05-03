import random
import pygame
import os
import constants

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMG_DIR    = os.path.join(ASSETS_DIR, "images")
SND_DIR    = os.path.join(ASSETS_DIR, "sounds")
IMG_DIR = "C:/Users/ernur/Desktop/myproject/python_base/TSIS3/images_and_sounds"
 
LANES = [
    constants.SCREEN_WIDTH // 2 - 133,
    constants.SCREEN_WIDTH // 2,
    constants.SCREEN_WIDTH // 2 + 133,
]
_SPAWN_GAP = 400


class RoadObject(pygame.sprite.Sprite):
    _registry: list = []

    @classmethod
    def clear_registry(cls):
        cls._registry.clear()

    def __init__(self):
        super().__init__()
        RoadObject._registry.append(self)

    def kill(self):
        if self in RoadObject._registry:
            RoadObject._registry.remove(self)
        super().kill()

    def _get_speed(self):
        """Переопределяется в подклассах."""
        return max(1, constants.SPEED)

    def _same_lane(self, other):
        half_self  = self.rect.width  // 2 + 8
        half_other = other.rect.width // 2 + 8
        return abs(self.rect.centerx - other.rect.centerx) < half_self + half_other

    def _moving_same_direction(self, other):
        self_oncoming  = getattr(self,  'kind', None) == 'oncoming'
        other_oncoming = getattr(other, 'kind', None) == 'oncoming'
        return not self_oncoming and not other_oncoming

    def _conflicts_with(self, other):
        if not self._same_lane(other):
            return False

        gap = _SPAWN_GAP 
        speed_diff = self._get_speed() - other._get_speed()
        if speed_diff > 0:
            gap += int(speed_diff * 60)

        return abs(self.rect.centery - other.rect.centery) < gap

    def _spawn(self, player_rect=None, lane=None, offset_y=None):
        available_lanes = LANES[:]
        random.shuffle(available_lanes)

        for attempt in range(100):
            if lane is not None:
                x = lane
                y = offset_y if offset_y is not None else random.randint(-400, -60)
            else:
                x = available_lanes[attempt % len(available_lanes)]
                y = random.randint(-400, -60)

            self.rect.center = (x, y)
            if player_rect and self.rect.colliderect(player_rect):
                continue
            if any(self._conflicts_with(o)
                   for o in RoadObject._registry if o is not self):
                continue

            return  

        self.rect.center = (available_lanes[0], -800)


    def _safe_speed(self):
        my_speed = self._get_speed()
        min_gap  = 130  

        for o in RoadObject._registry:
            if o is self:
                continue
            if not self._same_lane(o):
                continue
            if not self._moving_same_direction(o):
                continue 

            gap = o.rect.top - self.rect.bottom  
            if 0 < gap < min_gap:
                my_speed = min(my_speed, max(1, o._get_speed()))

        return my_speed

class Enemy(RoadObject):
    def __init__(self, kind=None, player_rect=None, lane=None):
        super().__init__()
        self.kind = kind or random.choice(['oncoming', 'traffic'])

        img_file = "Enemy1.png" if self.kind == 'oncoming' else "Enemy2.png"
        img_path = os.path.join(IMG_DIR, img_file)

        if os.path.exists(img_path):
            self.image = pygame.transform.scale(
                pygame.image.load(img_path).convert_alpha(), (50, 100)
            )
        else:
            self.image = pygame.Surface((50, 100), pygame.SRCALPHA)
            color = (220, 50, 50) if self.kind == 'oncoming' else (50, 50, 220)
            pygame.draw.rect(self.image, color, (0, 0, 50, 100), border_radius=6)
            f   = pygame.font.SysFont("Verdana", 18, bold=True)
            lbl = "▼" if self.kind == 'oncoming' else "▲"
            ls  = f.render(lbl, True, (255, 255, 255))
            self.image.blit(ls, ls.get_rect(center=(25, 50)))

        self.rect = self.image.get_rect()
        self._spawn(player_rect, lane)

    def _get_speed(self):
        if self.kind == 'oncoming':
            return constants.SPEED + 3
        return max(1, int(constants.SPEED * 0.55))

    def move(self):
        if self.kind == 'oncoming':
            speed = self._get_speed()
        else:
            speed = self._safe_speed()

        self.rect.move_ip(0, speed)
        if self.rect.top > constants.SCREEN_HEIGHT:
            self._spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self, car_color="yellow"):
        super().__init__()

        filepath = os.path.join(IMG_DIR, f"Player_{car_color}.png")
        if not os.path.exists(filepath):
            filepath = os.path.join(IMG_DIR, "Player_yellow.png")

        self.image = pygame.transform.scale(
            pygame.image.load(filepath).convert_alpha(), (50, 100)
        )
        self.draw_rect = self.image.get_rect()          
        self.rect = self.draw_rect.inflate(-15, -10)    
        self.rect.center = (constants.SCREEN_WIDTH // 2, 520)
        self.draw_rect.center = self.rect.center        

        self.lives            = 3
        self.shield_active    = False
        self.nitro_active     = False
        self.nitro_timer      = 0.0
        self.invincible_timer = 0.0

    def move(self):
        keys  = pygame.key.get_pressed()
        speed = 8 if self.nitro_active else 5
        if self.rect.left > 0 and keys[pygame.K_LEFT]:
            self.rect.move_ip(-speed, 0)
        if self.rect.right < constants.SCREEN_WIDTH and keys[pygame.K_RIGHT]:
            self.rect.move_ip(speed, 0)
        self.draw_rect.center = self.rect.center 

    def update_timers(self, dt):
        if self.nitro_active:
            self.nitro_timer -= dt
            if self.nitro_timer <= 0:
                self.nitro_active = False
                self.nitro_timer  = 0.0
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

    def take_hit(self):
        if self.invincible_timer > 0:
            return False
        if self.shield_active:
            self.shield_active    = False
            self.invincible_timer = 1.5
            return False
        self.lives -= 1
        self.invincible_timer = 1.5
        return self.lives <= 0

    def apply_powerup(self, kind):
        if kind == 'nitro':
            self.nitro_active = True
            self.nitro_timer  = 4.0
        elif kind == 'shield':
            self.shield_active = True
        elif kind == 'repair':
            self.lives = min(self.lives + 1, 3)


COIN_TIERS = [
    (0.70, 1, "Coin_gold.png"),
    (0.90, 2, "Coin_purple.png"),
    (1.00, 5, "Coin_red.png"),
]

class Coin(pygame.sprite.Sprite):
    def __init__(self, player_rect=None):
        super().__init__()
        roll       = random.random()
        self.value = 1
        chosen_img = "Coin_gold.png"
        for max_roll, value, img_name in COIN_TIERS:
            if roll < max_roll:
                self.value = value
                chosen_img = img_name
                break

        filepath = os.path.join(IMG_DIR, chosen_img)
        if os.path.exists(filepath):
            self.image = pygame.transform.scale(
                pygame.image.load(filepath).convert_alpha(), (40, 40)
            )
        else:
            colors = {1: (255,215,0), 2: (180,0,255), 5: (255,60,60)}
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, colors[self.value], (20, 20), 18)

        self.rect = self.image.get_rect()
        self._spawn(player_rect)

    def _spawn(self, player_rect=None):
        for _ in range(50):
            x = random.randint(40, constants.SCREEN_WIDTH - 40)
            y = random.randint(-200, -50)
            self.rect.center = (x, y)
            if player_rect is None or not self.rect.colliderect(player_rect):
                return

    def move(self):
        self.rect.move_ip(0, max(1, int(constants.SPEED // 1.5)))
        if self.rect.top > constants.SCREEN_HEIGHT:
            self._spawn()


POWERUP_STYLES = {
    'nitro':  {'bg': (255, 200,   0), 'fg': (0, 0, 0), 'letter': 'N'},
    'shield': {'bg': (  0, 180, 255), 'fg': (0, 0, 0), 'letter': 'S'},
    'repair': {'bg': (  0, 220,  80), 'fg': (0, 0, 0), 'letter': 'R'},
}
POWERUP_TIMEOUT = 8.0

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind=None, player_rect=None):
        super().__init__()
        self.kind  = kind or random.choice(list(POWERUP_STYLES.keys()))
        style      = POWERUP_STYLES[self.kind]
        size       = 40

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, style['bg'], (0, 0, size, size), border_radius=8)
        pygame.draw.rect(self.image, (255,255,255), (0, 0, size, size), 2, border_radius=8)
        f  = pygame.font.SysFont("Verdana", 22, bold=True)
        ls = f.render(style['letter'], True, style['fg'])
        self.image.blit(ls, ls.get_rect(center=(size//2, size//2)))

        self.rect     = self.image.get_rect()
        self.lifetime = POWERUP_TIMEOUT
        self._spawn(player_rect)

    def _spawn(self, player_rect=None):
        for _ in range(50):
            x = random.randint(40, constants.SCREEN_WIDTH - 40)
            self.rect.center = (x, -20)
            if player_rect is None or not self.rect.colliderect(player_rect):
                return

    def move(self, dt):
        self.rect.move_ip(0, max(1, int(constants.SPEED // 1.5)))
        self.lifetime -= dt
        if self.rect.top > constants.SCREEN_HEIGHT or self.lifetime <= 0:
            self.kill()


class Obstacle(RoadObject):
    def __init__(self, player_rect=None, lane=None, offset_y=None):
        super().__init__()

        spawn_roll = random.random()
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.kind  = 'empty'
        oil_path = os.path.join(IMG_DIR, "oil.png")
        if os.path.exists(oil_path) and spawn_roll < 0.4:
            self.kind  = 'oil'
            self.image = pygame.transform.scale(
                pygame.image.load(oil_path).convert_alpha(), (100, 40)
            )
        elif spawn_roll < 0.8:
            self.kind  = 'barrier'
            self.image = pygame.Surface((100, 28), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 80, 0), (0, 0, 100, 28), border_radius=6)
            f   = pygame.font.SysFont("Verdana", 13, bold=True)
            txt = f.render("BARRIER", True, (255, 255, 255))
            self.image.blit(txt, txt.get_rect(center=(50, 14)))
        
        self.rect = self.image.get_rect()
        self._spawn(player_rect, lane, offset_y)

    def _get_speed(self):
        return max(1, int(constants.SPEED * 0.8))

    def move(self):
        self.rect.move_ip(0, self._safe_speed())
        if self.rect.top > constants.SCREEN_HEIGHT:
            self._spawn()