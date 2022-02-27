from abc import ABC, abstractmethod, abstractproperty
import pygame


class Tile(ABC):

    plantable: bool
    frame: int

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
