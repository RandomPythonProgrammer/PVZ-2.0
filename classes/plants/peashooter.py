from classes.tiles.tile import Tile
from classes.worlds.world import World
from utils.class_loader import load_class, classes
from classes.plants.plant import Plant


@load_class
class Peashooter(Plant):

    @classmethod
    def can_plant(cls, tile: Tile, world: World) -> bool:
        return tile.type == 'normal'

    def on_create(self):
        self.timer = 0
        self.health = 200

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        if self.timer > 1.75:
            targets = [zombie for zombie in self.world.zombies
                       if not zombie.is_dead
                       and zombie.x > self.x
                       and abs(self.rect.bottom - zombie.rect.bottom) < self.world.tile_size]
            if len(targets) > 0:
                projectile = classes['projectile']['pea'](
                    self.x,
                    self.y,
                    self.world,
                    (200, 0),
                    source_y=self.rect.bottom,
                )
                projectile.x, projectile.y = self.x + self.rect.width/2, self.y + self.rect.height/4
                self.world.projectiles.append(projectile)
                self.timer = 0
        self.timer += dt

    def on_damage(self, damage: float, source: type) -> float:
        return damage
