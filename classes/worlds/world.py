from __future__ import annotations
from abc import ABC, abstractmethod
import pygame
from operator import attrgetter
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from classes.zombies.zombie import Zombie
    from classes.plants.plant import Plant
    from classes.objects.object import Object
    from classes.projectiles.projectile import Projectile
    from classes.tiles.tile import Tile


class World (ABC):
    """A class that contains all of the moving parts of the game"""

    game_id: str

    def __init__(self):
        self.game_over = False
        self.paused = False
        self.tiles: List[Tile] = []
        self.plants: List[Plant] = []
        self.zombies: List[Zombie] = []
        self.objects: List[Object] = []
        self.projectiles: List[Projectile] = []
        self.tile_size = 64
        self.columns = 0
        self.rows = 0
        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called on creation"""

    @abstractmethod
    def on_win(self):
        """Called when stage is won"""

    @abstractmethod
    def on_lose(self):
        """Called when stage is lost"""
        pass

    def update_all(self, dt: float):
        """Method for updating everything in the level"""
        [tile.update(dt) for tile in self.tiles]
        [object.update(dt) for object in self.objects]
        [plant.update(dt) for plant in self.plants]
        [zombie.update(dt) for zombie in self.zombies]
        [projectile.update(dt) for projectile in self.projectiles]

    @abstractmethod
    def on_wave(self):
        """Called when a wave starts"""

    @abstractmethod
    def spawn_sun(self):
        """Called when the world wants to spawn a sun, note you actually have to spawn the sun"""

    @abstractmethod
    def update(self, dt: float):
        """Called every loop, write the actions of the world here"""

    def render_all(self, surface: pygame.Surface):
        """Method for rendering everything in the world"""
        [tile.render(surface) for tile in sorted(self.tiles, key=attrgetter('y'))]
        [object.render(surface) for object in sorted(self.objects, key=attrgetter('y'))]
        [plant.render(surface) for plant in sorted(self.plants, key=attrgetter('y'))]
        [zombie.render(surface) for zombie in sorted(self.zombies, key=attrgetter('y'))]
        [projectile.render(surface) for projectile in sorted(self.projectiles, key=attrgetter('y'))]

    @abstractmethod
    def spawn_zombie(self, zombie: Zombie, is_wave: bool):
        """Method called when the game spawns a zombie"""

    @abstractmethod
    def render(self, surface: pygame.Surface):
        """Called every loop, write the rendering of the world here"""
