import pygame

ENEMY_SPEED = 2
GRAVITY = 0.5


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.assets = assets
        self.image = self.assets.get("hotdog.png")
        self.rect = self.image.get_rect(center=(x,y))

        self.vel_y = 0

    def update(self, player, level):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        on_platform = False
        for p in level.platforms:
            if self.rect.colliderect(p) and self.vel_y > 0:
                self.rect.bottom = p.top
                self.vel_y = 0
                on_platform = True

        if on_platform:
            if player.rect.centerx > self.rect.centerx:
                self.rect.x += ENEMY_SPEED
            else:
                self.rect.x -= ENEMY_SPEED
