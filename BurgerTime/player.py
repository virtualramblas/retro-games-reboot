import pygame

PLAYER_SPEED = 4
GRAVITY = 0.5


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, assets):
        super().__init__()
        self.assets = assets
        self.image = self.assets.get("player_1.png")
        self.rect = self.image.get_rect(center=pos)

        self.vel_y = 0
        self.lives = 3

        self.pepper = 5
        self.facing = 1  # 1 = right, -1 = left


    def reset_position(self, pos):
        self.rect.center = pos
        self.vel_y = 0

    def full_reset(self, start_pos):
        self.lives = 3
        self.pepper = 5
        self.vel_y = 0
        self.rect.center = start_pos


    def update(self, keys, level):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        on_platform = False
        for p in level.platforms:
            if self.rect.colliderect(p) and self.vel_y > 0:
                self.rect.bottom = p.top
                self.vel_y = 0
                on_platform = True

        if on_platform:
            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
                self.facing = -1

            if keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED
                self.facing = 1

