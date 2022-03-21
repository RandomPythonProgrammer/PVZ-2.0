from classes.tiles.tile import Tile
from classes.worlds.world import World
from utils.class_loader import load_class
from classes.farm_items.farm_item import FarmItem


@load_class
class BarbedWire(FarmItem):

    @classmethod
    def can_place(cls, tile: Tile, world: World) -> bool:
        return tile.type == 'normal'

    def on_create(self):
        self.health = 1500

    def on_death(self):
        self.destroy()

    def on_damage(self, damage: float, source: type) -> float:
        return damage

    def update(self, dt: float):
        pass
