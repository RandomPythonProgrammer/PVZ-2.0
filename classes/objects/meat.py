from utils.class_loader import load_class
from classes.objects.object import Object
from utils.globals import global_variables


@load_class
class Meat(Object):
    """Meat object"""

    bounding_box = (16, 16)

    def on_create(self):
        self.background = False
        self.timer = 0

    def on_death(self):
        self.destroy()

    def on_click(self, mouse_button: int):
        if mouse_button == 0:
            self.on_death()
            global_variables['money'] += 75

    def update(self, dt: float):
        if self.timer > 10:
            self.on_death()
        self.timer += dt

    def on_damage(self, damage: float, source: type):
        pass

