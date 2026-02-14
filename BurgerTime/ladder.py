import pygame

class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y_top, y_bottom, assets):
        super().__init__()
        height = y_bottom - y_top
        base_image = assets.get("ladder.png")
        self.image = pygame.transform.scale(base_image, (20, height))
        self.rect = self.image.get_rect(midtop=(x, y_top))

