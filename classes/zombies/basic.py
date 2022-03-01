from utils.class_loader import load_class
from classes.zombies.zombie import Zombie


@load_class
class Basic(Zombie):
    def on_create(self):
        self.health = 175

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        is_eating = False
        targets = [plant for plant in self.world.plants
                   if plant.collides(self)
                   and self.rect.centerx > plant.rect.centerx]
        if len(targets) > 0:
            targets[0].damage(45*dt, self)
            is_eating = True
        if not is_eating:
            self.move(-25 * dt, 0)

    def on_damage(self, damage: float, source: type) -> float:
        return damage
