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

        self.on_ladder = False
        self.climbing = False

    def reset_position(self, pos):
        self.rect.center = pos
        self.vel_y = 0

    def full_reset(self, start_pos):
        self.lives = 3
        self.pepper = 5
        self.vel_y = 0
        self.rect.center = start_pos


    def update(self, level, ladders, keys):
        ladder = self.check_ladder(ladders)

        # Start climbing
        if ladder and (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.climbing = True
            self.vel_y = 0

        # Climbing movement
        if self.climbing:
            if keys[pygame.K_UP]:
                self.rect.y -= PLAYER_SPEED
            elif keys[pygame.K_DOWN]:
                self.rect.y += PLAYER_SPEED

            # Stop climbing if leaving ladder bounds
            if not ladder or not ladder.rect.colliderect(self.rect):
                self.climbing = False

            return  # skip gravity while climbing

        if not self.climbing:
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

    def check_ladder(self, ladders):
        self.on_ladder = False

        for ladder in ladders:
            if self.rect.colliderect(ladder.rect):
                self.on_ladder = True
                return ladder

        return None
