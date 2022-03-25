from __future__ import annotations
from abc import ABC, abstractmethod
from utils.asset_loader import sprites
import pygame
from pygame.sprite import Sprite
from classes.tiles.tile import Tile
from typing import Tuple
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.worlds.world import World


class Belligerent (ABC, Sprite):
    """A zombie"""

    game_id: str
    bounding_box: Tuple[int, int]
    cost: int

    def __init__(self, x: int, y: int, team: int, world: World):
        super().__init__()
        self.is_dead = False
        self.visible = True
        self.frame = 0
        self.health = -1
        self.world = world
        self.team = team
        self._tile = None

        self.debug_image = pygame.Surface(self.bounding_box)
        self.debug_image.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 16)
        self.debug_image.blit(font.render(self.__class__.__name__, True, (0, 0, 0)), (0, 0))

        w, h = self.bounding_box
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.x, self.y = x, y
        self.has_collision = True

        self.on_create()

    @property
    def tile(self):
        return self._tile

    @tile.setter
    def tile(self, tile_object: Tile):
        self._tile = tile_object
        self.rect.center = tile_object.rect.center
        self.x = self.rect.x
        self.y = self.rect.y

    @classmethod
    @abstractmethod
    def can_place(cls, tile: Tile, world: World) -> bool:
        """Returns weather the belligerent can be placed or not"""

    @abstractmethod
    def on_create(self):
        """Called when the belligerent is created"""

    @abstractmethod
    def on_death(self):
        """Called when the belligerent dies or is removed"""

    def destroy(self):
        """Removes the belligerent from the world"""
        self.world.items.remove(self)
        self.kill()

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the belligerent here"""

    @abstractmethod
    def on_damage(self, damage: float, source: type) -> float:
        """Called when belligerent is damaged, return the amount of damage the belligerent takes"""

    def damage(self, damage: float, source: type):
        """Does damage to the belligerent and also calls on_death if it dies"""
        damage = self.on_damage(damage, source)
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True
            self.on_death()

    @property
    def image(self) -> pygame.Surface:
        try:
            return sprites[self.game_id][self.frame]
        except (KeyError, IndexError):
            return self.debug_image


    def move(self, x, y):
        """Moves the belligerent"""
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)

    def render(self, surface: pygame.Surface):
        if not self.visible:
            return
        if self.team == 1:
            surface.blit(self.image, (self.x, self.y))
        elif self.team == 2:
            surface.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
