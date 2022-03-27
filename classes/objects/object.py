from abc import ABC, abstractmethod
from utils.asset_loader import sprites
from classes.worlds.world import World
import pygame
from pygame.sprite import Sprite
from typing import Tuple


class Object(ABC, Sprite):
    """A projectile, specify a source y if the projectile is only supposed to hit on a certain y value, it will hit all
    except for its source_type"""

    game_id: str
    bounding_box: Tuple[int, int]

    def __init__(self, x: int, y: int, team: int, world: World):
        super().__init__()
        self.is_dead = False
        self.team = team
        self.frame = 0
        self.world = world
        self.has_collision = False
        self.background = True
        self.visible = True

        w, h = self.bounding_box
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)
        self.x, self.y = self.rect.topleft

        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called when the projectile is created"""

    @abstractmethod
    def on_death(self):
        """Called when the projectile dies or is removed"""

    def destroy(self):
        """Removes the projectile from the world"""
        self.world.items.remove(self)
        self.kill()

    @abstractmethod
    def on_click(self, mouse_button: int):
        """Called when the object is clicked"""

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the plant here"""

    def collides(self, rect: pygame.Rect) -> bool:
        """Returns whether it collides with the rectangle"""
        return self.rect.bottom == rect.bottom and self.rect.colliderect(rect)

    @property
    def image(self) -> pygame.Surface:
        try:
            return sprites[self.game_id][self.frame]
        except (KeyError, IndexError):
            debug_image = pygame.Surface(self.bounding_box)
            if self.team == 1:
                debug_image.fill((0, 0, 255))
            elif self.team == 2:
                debug_image.fill((255, 0, 0))
            font = pygame.font.SysFont(None, 16)
            debug_image.blit(font.render(self.__class__.__name__, True, (0, 0, 0)), (0, 0))
            return debug_image

    @abstractmethod
    def on_damage(self, damage: float, source: type):
        """called when damaged, return amount of damage the object takes"""

    def damage(self, damage: float, source: type):
        """Does damage to the object and also calls on_death if it dies"""
        damage = self.on_damage(damage, source)
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True
            self.on_death()

    def move(self, x, y):
        """Moves the projectile"""
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)

    def render(self, surface: pygame.Surface):
        if not self.visible:
            return
        if self.team == 2:
            surface.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))
