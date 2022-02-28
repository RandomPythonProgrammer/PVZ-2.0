from __future__ import annotations
from abc import ABC, abstractmethod
from classes.tiles.tile import Tile
from utils.asset_loader import sprites
from classes.worlds.world import World
import pygame
from pygame.sprite import Sprite


class Plant (ABC, Sprite):
    """A plant"""

    game_id: str

    def __init__(self, x: int, y: int, tile: Tile, world: World):
        super().__init__()
        self.is_dead = False
        self.frame = 0
        self.cost = 0
        self.cooldown = 0
        self.health = -1
        self.tile = tile
        self.world = world
        self.rect = self.image.get_rect()
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.x, self.y = x, y
        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called when the plant is created"""
        pass

    @abstractmethod
    def on_death(self):
        """Called when the plant dies or is removed"""
        pass

    def destroy(self):
        """Removes the plant from the world"""
        self.world.plants.remove(self)
        self.kill()

    @classmethod
    @abstractmethod
    def can_plant(cls, tile: Tile, world: World) -> bool:
        """Returns weather the plant can be planted or not"""
        pass

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the plant here"""
        pass

    def damage(self, damage: float):
        """Does damage to the plant and also calls on_death if it dies"""
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True
            self.on_death()

    def collides(self, sprite: pygame.sprite.Sprite) -> bool:
        """Returns whether the plant collides with a sprite"""
        return abs(self.rect.bottom - sprite.rect.bottom) < self.world.tile_size \
               and pygame.sprite.collide_mask(self, sprite)

    @property
    def image(self) -> pygame.Surface:
        return sprites[self.game_id][self.frame]

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, (self.x, self.y))
