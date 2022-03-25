import pygame.mouse
from utils.class_loader import load_class
from utils.input_utils import get_cancelled, set_cancelled, events
from classes.objects.object import Object
from utils.globals import global_variables


@load_class
class Egg(Object):
    """Egg object"""

    bounding_box = (16, 16)

    def on_create(self):
        self.background = False

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        if not get_cancelled():
            if pygame.MOUSEBUTTONUP in [event.type for event in events] and self.rect.collidepoint(pygame.mouse.get_pos()):
                x, y = pygame.mouse.get_pos()
                if pygame.mask.from_surface(self.image).get_at((x - self.x, y - self.y)) != 0:
                    set_cancelled(True)
                    self.on_death()
                    global_variables['money'] += 75

    def on_damage(self, damage: float, source: type):
        pass

