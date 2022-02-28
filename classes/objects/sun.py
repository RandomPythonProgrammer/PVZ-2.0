import pygame.mouse

from utils.class_loader import load_class
from utils.input_utils import is_cancelled, set_cancelled, events
from classes.objects.object import Object


@load_class
class Sun(Object):
    def on_create(self):
        pass

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        if not is_cancelled:
            if pygame.MOUSEBUTTONUP in events and self.rect.collidepoint(pygame.mouse.get_pos()):
                x, y = pygame.mouse.get_pos()
                if pygame.mask.from_surface(self.image).get_at((x - self.x, y - self.y)) != 0:
                    print("sun")
                    set_cancelled(True)
                    self.on_death()

    def on_damage(self, damage: float, source: type):
        pass
