from abc import ABC, abstractmethod
from utils.asset_loader import sprites
from classes.worlds.world import World
from pygame.sprite import Sprite
import pygame


class Tile(ABC, Sprite):

    game_id: str

    def __init__(self, x: int, y: int, world: World):
        super().__init__()
        self.type = 'null'
        self.frame = 0
        self.world = world
        self.rect = self.image.get_rect()
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.x, self.y = x, y
        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called on tile creation"""
        pass

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the tile here"""
        pass

    @property
    def image(self) -> pygame.Surface:
        return sprites[self.game_id][self.frame]
