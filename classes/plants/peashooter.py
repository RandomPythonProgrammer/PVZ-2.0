from classes.tiles.tile import Tile
from classes.worlds.world import World
from utils.class_loader import load_class, classes
from classes.plants.plant import Plant


@load_class(class_type='plants', game_id='peashooter')
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
        targets = [
            zombie for zombie in self.world.zombies if abs(self.rect.bottom - zombie.rect.bottom) < self.world.tile_size
        ]
        if self.timer > 3 and len(targets) > 0:
            self.world.projectiles.add(classes['projectiles']['pea'](
                self.x,
                self.y,
                self.world,
                (175, 0),
                source_y=self.rect.bottom,
            ))
            self.timer = 0
        self.timer += dt
