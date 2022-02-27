from abc import ABC, abstractmethod, abstractproperty
import pygame


class World (ABC):

    game_over: bool
    paused: bool

    tiles: list
    plants: list
    zombies: list
    objects: list

    def __init__(self):
        self.game_over = False
        self.paused = False
        self.tiles = []
        self.plants = []
        self.zombies = []
        self.objects = []
        self.on_create()

    @abstractmethod
    def on_create(self):
        pass

    @abstractmethod
    def on_win(self):
        pass

    @abstractmethod
    def on_lose(self):
        pass

    def update_all(self, dt: float):
        for object in self.objects:
            object.update(dt)
        for plant in self.plants:
            plant.update(dt)
        for zombie in self.zombies:
            zombie.update(dt)

    @abstractmethod
    def update(self, dt: float):
        pass

    def render_all(self, surface: pygame.Surface):
        for object in self.objects:
            object.render(surface)
        for plant in self.plants:
            plant.render(surface)
        for zombie in self.zombies:
            zombie.render(surface)

    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass

    @abstractmethod
    def spawn_zombie(self, zombie: Zombie, is_wave: bool):
        pass
