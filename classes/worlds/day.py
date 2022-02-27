import pygame

from classes.worlds.world import World
from classes.zombies.zombie import Zombie
from utils.class_loader import load_class, classes


@load_class(class_type='worlds', game_id='day')
class Day(World):
    def on_create(self):
        x, y = 0, 0
        for i in range(9):
            x = 0
            for j in range(12):
                tile = classes['tiles']['grass'](x, y, self)
                self.tiles.add(tile)
                x += tile.rect.width
            y += tile.rect.height

    def on_win(self):
        pass

    def on_lose(self):
        pass

    def update(self, dt: float):
        self.update_all(dt)

    def on_zombie_spawn(self, zombie: Zombie, is_wave: bool):
        pass

    def render(self, surface: pygame.Surface):
        self.render_all(surface)
