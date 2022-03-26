from classes.tiles.tile import Tile
from classes.worlds.world import World
from utils.class_loader import load_class, classes
from classes.farm_items.farm_item import FarmItem
from classes.belligerents.belligerent import Belligerent


@load_class
class ATDmk2(FarmItem):

    bounding_box = (64, 64)
    cost = 325

    @classmethod
    def can_place(cls, tile: Tile, world: World) -> bool:
        return tile.type == 'normal' and not tile.occupied

    def on_create(self):
        self.timer = 0
        self.health = 200

    def on_death(self):
        self.destroy()

    def on_click(self, mouse_button: int):
        pass

    def update(self, dt: float):
        if self.timer > 1.25:
            targets = [belligerent for belligerent in self.world.get_items(Belligerent)
                       if belligerent.team != self.team
                       and not belligerent.is_dead
                       and ((self.team == 1 and belligerent.x > self.x) or (self.team == 2 and belligerent.x < self.x))
                       and abs(self.rect.bottom - belligerent.rect.bottom) < self.world.row_spacing]
            if len(targets) > 0:
                if self.team == 1:
                    velocity = 200
                else:
                    velocity = -200
                projectile = classes['projectile']['bullet'](
                    self.x,
                    self.y,
                    self.world,
                    (velocity, 0),
                    self.team,
                    source_y=self.rect.bottom,
                )
                projectile.x, projectile.y = self.x + self.rect.width/2, self.y + self.rect.height/4
                self.world.items.append(projectile)
                self.timer = 0
        self.timer += dt

    def on_damage(self, damage: float, source: type) -> float:
        return damage
