import pygame
from enemy import Enemy
from ladder import Ladder
from ingredient import Ingredient

SCREEN_WIDTH = 800

LEVEL_DATA = {
    "player_start": (100, 100),

    "platforms": [
        (0, 150, 800, 10),
        (0, 250, 800, 10),
        (0, 350, 800, 10),
        (0, 450, 800, 10),
    ],

    "ladders": [
        (200, 150, 250),
        (400, 250, 350),
        (600, 350, 450),
    ],

    "enemies": [
        (700, 150),
        (600, 250),
    ]
}


class Level:
    def __init__(self, index, assets):
        self.assets = assets

        self.data = LEVEL_DATA

        self.player_start = self.data["player_start"]

        self.platforms = [pygame.Rect(p) for p in self.data["platforms"]]

        self.ladders = pygame.sprite.Group()
        for l in self.data["ladders"]:
            self.ladders.add(Ladder(*l, self.assets))

        self.enemies = pygame.sprite.Group()
        for e in self.data["enemies"]:
            self.enemies.add(Enemy(e[0], e[1], self.assets))

        self.ingredients = pygame.sprite.Group()

    def draw(self, screen):
        for p in self.platforms:
            pygame.draw.rect(screen, (255,255,255), p)

        self.ladders.draw(screen)

    def is_complete(self):
        return False  # placeholder for ingredient stacking logic
