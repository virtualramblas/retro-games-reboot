import pygame
from assets import Assets
from level import Level
from player import Player
from enemy import Enemy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYING = 0
RESPAWNING = 1
GAME_OVER = 2


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("BurgerTime")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)

        self.level_index = 0
        self.state = PLAYING
        self.respawn_timer = 0

        self.assets = Assets()

        # Load all sprites once
        self.assets.load("player_1.png", (40, 50))
        self.assets.load("hotdog.png", (40, 40))
        self.assets.load("pickle.png", (40, 40))
        self.assets.load("egg.png", (40, 40))
        self.assets.load("ladder.png", (20, 100))

        self.level = Level(self.level_index, self.assets)
        self.player = Player(self.level.player_start, self.assets)

        self.score = 0


    def load_level(self):
        self.level = Level(self.level_index, self.assets)
        self.player.reset_position(self.level.player_start)


    def update(self):
        keys = pygame.key.get_pressed()

        if self.state == PLAYING:
            self.player.update(keys, self.level)

            for enemy in self.level.enemies:
                enemy.update(self.player, self.level)

            if self.check_collisions():
                if self.player.lives <= 0:
                    self.state = GAME_OVER
                else:
                    self.state = RESPAWNING
                    self.respawn_timer = FPS * 2

            if self.level.is_complete():
                self.level_index += 1
                self.load_level()

        elif self.state == RESPAWNING:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.load_level()
                self.state = PLAYING

    def check_collisions(self):
        if pygame.sprite.spritecollideany(self.player, self.level.enemies):
            self.player.lives -= 1
            return True
        return False


    def draw(self):
        self.screen.fill((0, 0, 0))

        self.level.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

        for enemy in self.level.enemies:
            self.screen.blit(enemy.image, enemy.rect)

        self.draw_ui()

        if self.state == GAME_OVER:
            text = self.font.render("GAME OVER - Press R", True, (255, 0, 0))
            self.screen.blit(text, (250, 280))

        pygame.display.flip()

    def draw_ui(self):
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, (255,255,255))
        score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        pepper_text = self.font.render(f"Pepper: {self.player.pepper}", True, (255,255,255))

        self.screen.blit(lives_text, (10, 10))
        self.screen.blit(score_text, (10, 40))
        self.screen.blit(pepper_text, (10, 70))


    def use_pepper(self):
        if self.player.pepper <= 0:
            return

        self.player.pepper -= 1

        spray_range = 80
        spray_rect = pygame.Rect(
            self.player.rect.centerx,
            self.player.rect.centery - 10,
            spray_range * self.player.facing,
            20
        )

        # Normalize rect if facing left
        if self.player.facing < 0:
            spray_rect.x -= spray_range
            spray_rect.width = spray_range

        for enemy in self.level.enemies:
            if spray_rect.colliderect(enemy.rect):
                enemy.freeze()


    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == PLAYING:
                        self.use_pepper()

                    if event.key == pygame.K_r and self.state == GAME_OVER:
                        self.score = 0
                        self.level_index = 0
                        self.load_level()
                        self.player.full_reset(self.level.player_start)
                        self.state = PLAYING


            self.update()
            self.draw()

        pygame.quit()
