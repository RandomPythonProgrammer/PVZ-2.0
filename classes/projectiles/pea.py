from utils.class_loader import load_class
from classes.projectiles.projectile import Projectile
import time


@load_class
class Pea(Projectile):
    def on_create(self):
        self.damage = 25
        self.start_time = time.time()

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        collisions = self.get_collisions()
        if len(collisions) > 0:
            collisions[0].damage(self.damage, self)
            self.on_death()
            return
        x, y = self.velocity
        self.move(x*dt, y)
        if time.time() - self.start_time > 10:
            self.on_death()
