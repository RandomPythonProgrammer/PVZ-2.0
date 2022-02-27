from __future__ import annotations
from abc import ABC, abstractmethod
import pygame
from pygame.sprite import Group
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.zombies.zombie import Zombie


class World (ABC):
    """A class that contains all of the moving parts of the game"""

    game_id: str

    def __init__(self):
        self.game_over = False
        self.paused = False
        self.tiles = Group()
        self.plants = Group()
        self.zombies = Group()
        self.objects = Group()
        self.projectiles = Group()
        self.tile_size = 64
        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called on creation"""
        pass

    @abstractmethod
    def on_win(self):
        """Called when stage is won"""
        pass

    @abstractmethod
    def on_lose(self):
        """Called when stage is lost"""
        pass

    def update_all(self, dt: float):
        """Method for updating everything in the level"""
        for tile in self.tiles:
            tile.update(dt)
        for object in self.objects:
            object.update(dt)
        for plant in self.plants:
            plant.update(dt)
        for zombie in self.zombies:
            zombie.update(dt)
        for projectile in self.projectiles:
            projectile.update(dt)

    @abstractmethod
    def update(self, dt: float):
        """Called every loop, write the actions of the world here"""
        pass

    def render_all(self, surface: pygame.Surface):
        """Method for rendering everything in the world"""
        self.tiles.draw(surface)
        self.objects.draw(surface)
        self.plants.draw(surface)
        self.zombies.draw(surface)
        self.projectiles.draw(surface)

    @abstractmethod
    def on_zombie_spawn(self, zombie: Zombie, is_wave: bool):
        """Method called when the game spawns a zombie"""
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
        """Called every loop, write the rendering of the world here"""
        pass
