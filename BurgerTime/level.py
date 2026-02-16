import pygame
from enemy import Enemy
from ladder import Ladder
from ingredient import Ingredient

SCREEN_WIDTH = 800

class Level:
    def __init__(self, data, assets):
        self.assets = assets

        #self.data = LEVELS
        self.data = data

        self.player_start = self.data["player_start"]

        self.platforms = [pygame.Rect(p) for p in self.data["platforms"]]

        self.ladders = pygame.sprite.Group()
        for l in self.data["ladders"]:
            self.ladders.add(Ladder(*l, self.assets))

        self.enemies = pygame.sprite.Group()
        for e in self.data["enemies"]:
            self.enemies.add(Enemy(e[0], e[1], self.assets))

        self.ingredients = pygame.sprite.Group()
        self.load_ingredients(self.data["ingredients"])


    def draw(self, screen):
        for p in self.platforms:
            pygame.draw.rect(screen, (255,255,255), p)

        self.ladders.draw(screen)
        self.ingredients.draw(screen)

    def is_complete(self):
        return False  # placeholder for ingredient stacking logic
    
    def load_ingredients(self, layout_data):
        for name, x, y in layout_data:
            ingredient = Ingredient(x, y, self.assets.get(name))
            self.ingredients.add(ingredient)
