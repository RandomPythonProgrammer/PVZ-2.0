from __future__ import annotations
from abc import ABC, abstractmethod
import pygame
from utils.view_utils import ViewPort
from operator import attrgetter
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from classes.belligerents.belligerent import Belligerent
    from classes.farm_items.farmitem import FarmItem
    from classes.objects.object import Object
    from classes.projectiles.projectile import Projectile
    from classes.tiles.tile import Tile


class World (ABC):
    """A class that contains all of the moving parts of the game"""

    game_id: str

    def __init__(self, view_port: ViewPort):
        self.view_port: ViewPort = view_port
        self.game_over = False
        self.paused = False
        self.tiles: List[Tile] = []
        self.farm_items: List[FarmItem] = []
        self.belligerents: List[Belligerent] = []
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
        [plant.update(dt) for plant in self.farm_items]
        [zombie.update(dt) for zombie in self.belligerents]
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
        temp_surface = pygame.Surface((self.view_port.width, self.view_port.height))
        [tile.render(temp_surface) for tile in sorted(self.tiles, key=attrgetter('y'))]
        [object.render(temp_surface) for object in sorted(self.objects, key=attrgetter('y')) if object.background]
        [plant.render(temp_surface) for plant in sorted(self.farm_items, key=attrgetter('y'))]
        [projectile.render(temp_surface) for projectile in sorted(self.projectiles, key=attrgetter('y'))]
        [zombie.render(temp_surface) for zombie in sorted(self.belligerents, key=attrgetter('y'))]
        [object.render(temp_surface) for object in sorted(self.objects, key=attrgetter('y')) if not object.background]
        surface.blit(temp_surface, self.view_port.project(0, 0))

    @abstractmethod
    def spawn_belligerent(self, belligerent: Belligerent, is_wave: bool):
        """Method called when the game spawns a zombie"""

    def render(self, surface: pygame.Surface):
        """Renders the world"""
        self.on_render(surface)
        self.render_all(surface)

    @abstractmethod
    def on_render(self, surface: pygame.Surface):
        """Called every loop, write the rendering of the world here"""
