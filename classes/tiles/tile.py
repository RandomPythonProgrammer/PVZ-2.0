from abc import ABC, abstractmethod
from utils.asset_loader import sprites
from classes.worlds.world import World
from pygame.sprite import Sprite
import pygame
from typing import Tuple


class Tile(ABC, Sprite):

    game_id: str
    bounding_box: Tuple[int, int]

    def __init__(self, x: int, y: int, world: World):
        super().__init__()
        self.type = 'null'
        self.frame = 0
        self.world = world
        self.visible = True
        self.has_collision = False

        w, h = self.bounding_box
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.x, self.y = x, y
        self.occupied = False

        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called on tile creation"""

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the tile here"""

    @property
    def image(self) -> pygame.Surface:
        try:
            return sprites[self.game_id][self.frame]
        except (KeyError, IndexError):
            debug_image = pygame.Surface(self.bounding_box)
            debug_image.fill((255, 255, 255))
            font = pygame.font.SysFont(None, 16)
            debug_image.blit(font.render(self.__class__.__name__, True, (0, 0, 0)), (0, 0))
            return debug_image

    def render(self, surface: pygame.Surface):
        if not self.visible:
            return
        surface.blit(self.image, (self.x, self.y))
