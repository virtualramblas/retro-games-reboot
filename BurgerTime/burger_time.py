import pygame
import sys
import os
import random

pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 4
ENEMY_SPEED = 2
GRAVITY = 6

PLATFORM_Y = [100, 200, 300, 400, 500]
platforms = []
for y in PLATFORM_Y:
    platforms.append(pygame.Rect(0, y + 50, SCREEN_WIDTH, 10))

game_over = False

# --- Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BurgerTime - Sprite Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

ASSET_PATH = "assets"

def load_image(name, scale=None):
    image = pygame.image.load(os.path.join(ASSET_PATH, name)).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

# --- Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [
            load_image("player_1.png", (40, 50)),
            load_image("player_2.png", (40, 50))
        ]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(100, PLATFORM_Y[0]))

        self.vel_y = 0
        self.on_platform = False
        self.on_ladder = False
        self.climbing = False

        self.score = 0
        self.lives = 3
        self.pepper = 5

        self.animation_timer = 0
        self.current_frame = 0

        self.invulnerable = False
        self.invuln_timer = 0
        self.alive = True


    def update(self, keys, platforms, ladders):
        self.on_platform = False
        self.on_ladder = False

        # --- Ladder Detection ---
        ladder_hits = pygame.sprite.spritecollide(self, ladders, False)
        if ladder_hits:
            self.on_ladder = True

        # --- Vertical Movement ---
        if self.on_ladder and (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.climbing = True
            self.vel_y = 0

            ladder = ladder_hits[0]
            self.rect.centerx = ladder.rect.centerx

            if keys[pygame.K_UP]:
                self.rect.y -= PLAYER_SPEED
            if keys[pygame.K_DOWN]:
                self.rect.y += PLAYER_SPEED
        else:
            self.climbing = False

        # --- Gravity ---
        if not self.climbing:
            self.vel_y += 0.5
            self.rect.y += self.vel_y

        # --- Platform Collision ---
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_platform = True

        # --- Horizontal Movement ---
        if self.on_platform:
            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED

        self.rect.clamp_ip(screen.get_rect())

        # --- Animation ---
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.animation_timer += 1
            if self.animation_timer > 10:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.animation_timer = 0

        # Handle invulnerability timer
        if self.invulnerable:
            self.invuln_timer -= 1
            if self.invuln_timer <= 0:
                self.invulnerable = False

            
    def spray(self, enemies):
        if self.pepper <= 0:
            return
        self.pepper -= 1
        for enemy in enemies:
            if abs(enemy.rect.x - self.rect.x) < 60 and abs(enemy.rect.y - self.rect.y) < 40:
                enemy.freeze()

    def hit(self):
        if self.invulnerable or not self.alive:
            return

        self.lives -= 1
        self.invulnerable = True
        self.invuln_timer = 120  # 2 seconds at 60 FPS

        if self.lives <= 0:
            self.alive = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_name):
        super().__init__()
        self.image = load_image(sprite_name, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.frozen = False
        self.freeze_timer = 0

    def update(self, player):
        if self.frozen:
            self.freeze_timer -= 1
            if self.freeze_timer <= 0:
                self.frozen = False
            return

        if self.rect.x < player.rect.x:
            self.rect.x += ENEMY_SPEED
        elif self.rect.x > player.rect.x:
            self.rect.x -= ENEMY_SPEED

        if self.rect.y < player.rect.y:
            self.rect.y += ENEMY_SPEED
        elif self.rect.y > player.rect.y:
            self.rect.y -= ENEMY_SPEED

    def freeze(self):
        self.frozen = True
        self.freeze_timer = FPS * 2

class Ingredient(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_name):
        super().__init__()
        self.image = load_image(sprite_name, (100, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.falling = False

    def update(self):
        if self.falling:
            self.rect.y += GRAVITY
            for level in PLATFORM_Y:
                if self.rect.y >= level:
                    self.rect.y = level
                    self.falling = False
                    break

class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y_top, y_bottom):
        super().__init__()
        height = y_bottom - y_top
        self.image = load_image("ladder.png", (40, height))
        self.rect = self.image.get_rect(midtop=(x, y_top))

ladders = pygame.sprite.Group(
        Ladder(200, PLATFORM_Y[0] + 50, PLATFORM_Y[1] + 50),
        Ladder(400, PLATFORM_Y[1] + 50, PLATFORM_Y[2] + 50),
        Ladder(600, PLATFORM_Y[2] + 50, PLATFORM_Y[3] + 50),
        Ladder(300, PLATFORM_Y[3] + 50, PLATFORM_Y[4] + 50),
    )

# --- Game Setup ---

player = Player()

enemies = pygame.sprite.Group(
    Enemy(700, PLATFORM_Y[0], "hotdog.png"),
    Enemy(600, PLATFORM_Y[1], "pickle.png"),
    Enemy(650, PLATFORM_Y[2], "egg.png")
)

ingredients = pygame.sprite.Group(
    Ingredient(200, PLATFORM_Y[0], "bun_top.png"),
    Ingredient(350, PLATFORM_Y[1], "lettuce.png"),
    Ingredient(500, PLATFORM_Y[2], "patty.png"),
    Ingredient(250, PLATFORM_Y[3], "bun_bottom.png")
)

all_sprites = pygame.sprite.Group(player, enemies, ingredients)

# --- Helper Functions ---

def draw_platforms():
    for y in PLATFORM_Y:
        pygame.draw.line(screen, (255,255,255), (0, y + 50), (SCREEN_WIDTH, y + 50), 2)

def check_ingredient_drop():
    for ingredient in ingredients:
        if player.rect.colliderect(ingredient.rect) and not ingredient.falling:
            ingredient.falling = True
            player.score += 50

def check_enemy_drop():
    for ingredient in ingredients:
        if ingredient.falling:
            for enemy in enemies:
                if ingredient.rect.colliderect(enemy.rect):
                    enemy.rect.y = 0
                    player.score += 500

def check_collisions():
    if pygame.sprite.spritecollideany(player, enemies):
        player.hit()

def draw_ui():
    screen.blit(font.render(f"Score: {player.score}", True, (255,255,255)), (10, 10))
    screen.blit(font.render(f"Lives: {player.lives}", True, (255,255,255)), (10, 35))
    screen.blit(font.render(f"Pepper: {player.pepper}", True, (255,255,255)), (10, 60))

def draw_game_over():
    text1 = font.render("GAME OVER", True, (255, 50, 50))
    text2 = font.render("Press R to Restart", True, (255, 255, 255))

    screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, SCREEN_HEIGHT//2 - 40))
    screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, SCREEN_HEIGHT//2))

# --- Main Loop ---

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.spray(enemies)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                player.lives = 3
                player.alive = True
                player.invulnerable = False
                player.rect.center = (100, PLATFORM_Y[0])
                game_over = False


    if not player.alive:
        game_over = True

    if not game_over:
        player.update(keys, platforms, ladders)
        enemies.update(player)
        ingredients.update()

        check_ingredient_drop()
        check_enemy_drop()
        check_collisions()

    if game_over:
        draw_game_over()

    draw_platforms()
    ladders.draw(screen)
    all_sprites.draw(screen)
    draw_ui()

    pygame.display.flip()

pygame.quit()
sys.exit()