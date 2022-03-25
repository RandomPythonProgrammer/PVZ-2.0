from utils.class_loader import load_class
from classes.projectiles.projectile import Projectile


@load_class
class Bullet(Projectile):

    bounding_box = (16, 16)

    def on_create(self):
        self.damage = 25
        self.time = 0

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        self.time += dt
        collisions = self.get_collisions()
        if len(collisions) > 0:
            collisions[0].damage(self.damage, self)
            self.on_death()
            return
        x, y = self.velocity
        self.move(x*dt, y*dt)
        if self.time > 10:
            self.on_death()
