from classes.tiles.tile import Tile
from classes.worlds.world import World
from utils.class_loader import load_class
from classes.belligerents.belligerent import Belligerent
from classes.farm_items.farm_item import FarmItem


@load_class
class Basic(Belligerent):

    bounding_box = (64, 128)
    cost = 150

    @classmethod
    def can_place(cls, tile: Tile, world: World) -> bool:
        return tile.type == 'normal'

    def on_create(self):
        self.health = 175

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        is_eating = False
        targets = [target for target in self.world.get_items(FarmItem)
                   if target.collides(self)
                   and abs(target.rect.bottom - self.rect.bottom) < self.world.row_spacing
                   and self.rect.centerx > target.rect.centerx
                   and target.team != self.team]
        if len(targets) > 0:
            targets[0].damage(45*dt, self)
            is_eating = True
        if not is_eating:
            if self.team == 1:
                velocity = 25
            else:
                velocity = -25
            self.move(velocity * dt, 0)

    def on_damage(self, damage: float, source: type) -> float:
        return damage
