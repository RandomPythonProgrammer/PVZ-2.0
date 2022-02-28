from classes.tiles.tile import Tile
from utils.class_loader import load_class


@load_class
class Grass(Tile):
    def on_create(self):
        self.type = 'normal'

    def update(self, dt: float):
        pass
