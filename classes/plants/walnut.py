from classes.tiles.tile import Tile
from classes.worlds.world import World
from utils.class_loader import load_class
from classes.plants.plant import Plant


@load_class(class_type='plants', game_id='walnut')
class Walnut(Plant):

    @classmethod
    def can_plant(cls, tile: Tile, world: World) -> bool:
        return tile.type == 'normal'

    def on_create(self):
        self.health = 1250

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        pass
