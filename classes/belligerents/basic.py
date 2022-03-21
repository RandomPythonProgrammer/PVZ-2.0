from utils.class_loader import load_class
from classes.belligerents.belligerent import Belligerent


@load_class
class Basic(Belligerent):
    def on_create(self):
        self.health = 175

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        is_eating = False
        targets = [target for target in self.world.farm_items
                   if target.collides(self)
                   and self.rect.centerx > target.rect.centerx
                   and target.team != self.team]
        if len(targets) > 0:
            targets[0].damage(45*dt, self)
            is_eating = True
        if not is_eating:
            self.move(-25 * dt, 0)

    def on_damage(self, damage: float, source: type) -> float:
        return damage
