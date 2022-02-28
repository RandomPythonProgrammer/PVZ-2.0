from classes.worlds.world import World
from utils.class_loader import load_class, classes
import pygame
import random


@load_class
class Day(World):
    def on_create(self):
        self.columns = 12
        self.rows = 9
        x, y = 0, self.tile_size
        for i in range(self.rows):
            x = 0
            for j in range(self.columns):
                tile = classes['tile']['grass'](x, y, self)
                self.tiles.append(tile)
                x += self.tile_size
            y += self.tile_size

    def on_win(self):
        pass

    def on_lose(self):
        pass

    def on_wave(self):
        pass

    def update(self, dt: float):
        self.update_all(dt)

    def spawn_zombie(self, zombie: type, is_wave: bool):
        self.zombies.append(zombie((self.columns-1) * self.tile_size, random.randint(0, self.rows-1) * self.tile_size, self))

    def render(self, surface: pygame.Surface):
        self.render_all(surface)
