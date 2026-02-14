import pygame
import os

ASSET_PATH = "assets"

class Assets:
    def __init__(self):
        self.images = {}

    def load(self, name, scale=None):
        image = pygame.image.load(os.path.join(ASSET_PATH, name)).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        self.images[name] = image
        return image

    def get(self, name):
        return self.images.get(name)
