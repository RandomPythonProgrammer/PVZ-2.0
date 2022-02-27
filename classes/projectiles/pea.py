from utils.class_loader import load_class
from classes.projectiles.projectile import Projectile


@load_class(class_type='projectiles', game_id='pea')
class Pea(Projectile):
    def on_create(self):
        pass

    def on_death(self):
        pass

    def update(self, dt: float):
        collisions = self.get_collisions()
        if len(collisions) > 0:
            collisions[0].damage(15)
            self.destroy()
            return
        x, y = self.velocity
        self.move(x*dt, y)
