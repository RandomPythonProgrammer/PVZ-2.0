from classes.tiles.tile import Tile
from classes.worlds.world import World
from utils.class_loader import load_class, classes
from classes.farm_items.farm_item import FarmItem
import random


@load_class
class Tomato(FarmItem):

    bounding_box = (64, 64)
    cost = 100

    @classmethod
    def can_place(cls, tile: Tile, world: World) -> bool:
        return tile.type == 'normal' and not tile.occupied

    def on_create(self):
        self.timer = 0
        self.health = 75

    def on_death(self):
        self.destroy()

    def on_click(self, mouse_button: int):
        pass

    def update(self, dt: float):
        if self.timer > 7.75:
            x, y, w, h = self.tile.rect
            self.world.items.append(classes['object']['produce'](
                random.randint(x, x+w),
                random.randint(y, y+h),
                self.team,
                self.world
            ))
            self.timer = 0
        self.timer += dt

    def on_damage(self, damage: float, source: type) -> float:
        return damage
