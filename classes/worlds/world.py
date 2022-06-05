from __future__ import annotations
from abc import ABC, abstractmethod
import pygame
from utils.view_utils import ViewPort
from operator import attrgetter
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from classes.belligerents.belligerent import Belligerent
    from classes.tiles.tile import Tile


class World (ABC):
    """A class that contains all of the moving parts of the game"""

    game_id: str

    def __init__(self, view_port: ViewPort):
        self.view_port: ViewPort = view_port
        self.game_over = False
        self.paused = False
        self.tiles: List[Tile] = []
        self.items: List[object] = []
        self.columns = 0
        self.rows = 0
        self.is_wave = False
        self.belligerent_queue = {}
        self.current_wave = 0
        self.on_create()
        self.row_spacing = 64

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
        [item.update(dt) for item in self.items]
        [tile.update(dt) for tile in self.tiles]

    @abstractmethod
    def on_wave(self):
        """Called when a wave starts"""

    @abstractmethod
    def update(self, dt: float):
        """Called every loop, write the actions of the world here"""

    def render_all(self, surface: pygame.Surface):
        """Method for rendering everything in the world"""
        temp_surface = pygame.Surface((self.view_port.width, self.view_port.height))
        [item.render(temp_surface) for item in sorted(self.items, key=attrgetter('rect.bottom')) if hasattr(item, 'background') and item.background]
        [item.render(temp_surface) for item in sorted(self.tiles, key=attrgetter('rect.bottom'))]
        [item.render(temp_surface) for item in sorted(self.items, key=attrgetter('rect.bottom')) if not hasattr(item, 'background')]
        [item.render(temp_surface) for item in sorted(self.items, key=attrgetter('rect.bottom')) if hasattr(item, 'background') and not item.background]
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

    def get_items(self, item_types: List[type]):
        """Return all items of a certain type"""
        if type(item_types) != list:
            item_types = [item_types]
        return [item for item in self.items if len([True for item_type in item_types if isinstance(item, item_type)]) > 0]

    def is_base(self, item: object, type_str: str):
        base = item.__class__.__base__
        while base != object:
            if base.__name__.lower() == type_str:
                return True
            base = base.__base__
