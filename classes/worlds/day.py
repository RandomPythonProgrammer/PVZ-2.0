from classes.worlds.world import World
from utils.class_loader import load_class, classes
import pygame
import random


@load_class
class Day(World):
    def on_create(self):
        self.columns = 12
        self.rows = 9
        w, h = classes['tile']['grass'].bounding_box
        x, y = 0, h
        for i in range(self.rows):
            x = 0
            for j in range(self.columns):
                tile = classes['tile']['grass'](x, y, self)
                self.items.append(tile)
                x += w
            y += h

    def on_win(self):
        pass

    def on_lose(self):
        pass

    def on_wave(self):
        pass

    def update(self, dt: float):
        self.update_all(dt)

    def spawn_belligerent(self, belligerent: type, is_wave: bool):
        self.items.append(belligerent((self.columns - 1) * self.row_spacing, random.randint(0, self.rows - 1) * self.row_spacing, 2, self))

    def on_render(self, surface: pygame.Surface):
        pass
