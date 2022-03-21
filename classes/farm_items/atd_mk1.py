from classes.tiles.tile import Tile
from classes.worlds.world import World
from utils.class_loader import load_class, classes
from classes.farm_items.farm_item import FarmItem


@load_class
class ATDmk1(FarmItem):

    @classmethod
    def can_place(cls, tile: Tile, world: World) -> bool:
        return tile.type == 'normal'

    def on_create(self):
        self.timer = 0
        self.health = 200

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        if self.timer > 1.75:
            targets = [belligerent for belligerent in self.world.belligerents
                       if belligerent.team != self.team
                       and not belligerent.is_dead
                       and belligerent.x > self.x
                       and abs(self.rect.bottom - belligerent.rect.bottom) < self.world.tile_size]
            if len(targets) > 0:
                projectile = classes['projectile']['bullet'](
                    self.x,
                    self.y,
                    self.world,
                    (200, 0),
                    self.team,
                    source_y=self.rect.bottom,
                )
                projectile.x, projectile.y = self.x + self.rect.width/2, self.y + self.rect.height/4
                self.world.projectiles.append(projectile)
                self.timer = 0
        self.timer += dt

    def on_damage(self, damage: float, source: type) -> float:
        return damage
