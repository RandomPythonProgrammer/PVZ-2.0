from abc import ABC, abstractmethod, abstractproperty
from classes.tiles.tile import Tile
import pygame


class Plant (ABC):

    is_dead: int
    frame: int
    cost: int
    cooldown: int
    health: int
    tile: Tile

    def __init__(self):
        pass

    @abstractmethod
    def on_create(self):
        pass

    @abstractmethod
    def on_death(self):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface):
        pass
