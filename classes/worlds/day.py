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

    def spawn_sun(self):
        self.objects.append(classes['object']['sun'](
            random.random()*self.columns*self.tile_size,
            random.random()*(self.rows+1)*self.tile_size,
            3,
            self,
        ))

    def update(self, dt: float):
        self.update_all(dt)

    def spawn_belligerent(self, belligerent: type, is_wave: bool):
        self.belligerents.append(belligerent((self.columns - 1) * self.tile_size, random.randint(0, self.rows - 1) * self.tile_size, 2, self))

    def on_render(self, surface: pygame.Surface):
        pass
