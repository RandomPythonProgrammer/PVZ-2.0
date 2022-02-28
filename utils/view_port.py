import pygame


class ViewPort(pygame.Surface):
    def __init__(self, x: float, y: float, width: float, height: float, x_offset: float, y_offset: float):
        super(ViewPort, self).__init__((width, height))
        self.get_offset()
        self.x = x
        self.y = y

    def project(self, x: float, y: float) -> tuple:
        return x - self.x, y - self.y
