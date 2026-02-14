import pygame

class Ingredient(pygame.sprite.Sprite):
    def __init__(self, x, y, assets):
        super().__init__()
        self.image = assets.get("bun_top.png")

