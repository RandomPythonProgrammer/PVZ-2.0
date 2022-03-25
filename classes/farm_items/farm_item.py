from abc import ABC, abstractmethod
from classes.tiles.tile import Tile
from utils.asset_loader import sprites
from classes.worlds.world import World
import pygame
from pygame.sprite import Sprite
from typing import Tuple


class FarmItem(ABC, Sprite):
    """A farm item"""

    game_id: str
    bounding_box: Tuple[int, int]
    cost: int
    growth_time: float

    def __init__(self, x: int, y: int, team: int, world: World):
        super().__init__()
        self.is_dead = False
        self.frame = 0
        self.cost = 0
        self.cooldown = 0
        self.visible = True
        self.health = -1
        self._tile = None
        self.world = world
        self.team = team

        self.debug_image = pygame.Surface(self.bounding_box)
        if self.team == 1:
            self.debug_image.fill((0, 0, 255))
        elif self.team == 2:
            self.debug_image.fill((255, 0, 0))
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
        self._tile.occupied = True

    @abstractmethod
    def on_click(self, mouse_button: int):
        """Called when the object is clicked"""

    @abstractmethod
    def on_create(self):
        """Called when the farm item is created"""

    @abstractmethod
    def on_death(self):
        """Called when the farm item dies or is removed"""

    def destroy(self):
        """Removes the farm item from the world"""
        self.world.items.remove(self)
        self.tile.occupied = False
        self.kill()

    @classmethod
    @abstractmethod
    def can_place(cls, tile: Tile, world: World) -> bool:
        """Returns weather the farm item can be placed or not"""

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the farm item here"""

    @abstractmethod
    def on_damage(self, damage: float, source: type) -> float:
        """Called when zombie is damaged, return the amount of damage the zombie takes"""

    def damage(self, damage: float, source: type):
        """Does damage to the farm item and also calls on_death if it dies"""
        self.health -= self.on_damage(damage, source)
        if self.health <= 0:
            self.is_dead = True
            self.on_death()

    def collides(self, sprite: pygame.sprite.Sprite, lane: bool = False) -> bool:
        """Returns whether the farm item collides with a sprite"""
        return (abs(self.rect.bottom - sprite.rect.bottom) < self.world.row_spacing or not lane) \
            and sprite.rect.colliderect(self.rect)

    @property
    def image(self) -> pygame.Surface:
        try:
            return sprites[self.game_id][self.frame]
        except (KeyError, IndexError):
            return self.debug_image

    def render(self, surface: pygame.Surface):
        if not self.visible:
            return
        if self.team == 1:
            surface.blit(self.image, (self.x, self.y))
        elif self.team == 2:
            surface.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
