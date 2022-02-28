from utils.class_loader import load_class
from classes.zombies.zombie import Zombie
import pygame


@load_class(class_type='zombies', game_id='basic')
class Basic(Zombie):
    def on_create(self):
        self.health = 200

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        is_eating = False
        targets = [plant for plant in self.world.plants if plant.collides(self)]
        if len(targets) > 0:
            targets[0].damage(45*dt)
            is_eating = True
        if not is_eating:
            self.move(-25 * dt, 0)

    def on_damage(self, damage: float) -> float:
        return damage
