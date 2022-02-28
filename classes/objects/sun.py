import pygame.mouse
from utils.class_loader import load_class
from utils.input_utils import get_cancelled, set_cancelled, events
from classes.objects.object import Object


@load_class
class Sun(Object):
    """Sun object, you will have to set speed to zero if you don't want it to fall"""
    def on_create(self):
        self.background = False
        self.__dropped = False
        self.speed = 40
        self.target_x = self.x
        self.target_y = self.y

    def on_death(self):
        self.destroy()

    def update(self, dt: float):
        if not get_cancelled():
            if pygame.MOUSEBUTTONUP in [event.type for event in events] and self.rect.collidepoint(pygame.mouse.get_pos()):
                x, y = pygame.mouse.get_pos()
                if pygame.mask.from_surface(self.image).get_at((x - self.x, y - self.y)) != 0:
                    set_cancelled(True)
                    self.on_death()

        if self.speed == 0:
            return

        if not self.__dropped:
            self.__dropped = True
            self.y = 0

        if abs(self.target_x - self.x) < 2:
            self.x = self.target_x
        if abs(self.target_y - self.y) < 2:
            self.y = self.target_y
        if self.target_x == self.x and self.target_y == self.y:
            self.speed = 0
        if self.x > self.target_x:
            self.move(-self.speed*dt, 0)
        else:
            self.move(self.speed*dt, 0)
        if self.y > self.target_y:
            self.move(0, -self.speed*dt)
        else:
            self.move(0, self.speed*dt)

    def on_damage(self, damage: float, source: type):
        pass

