from abc import ABC, abstractmethod
from utils.asset_loader import sprites
from utils.display_utils import update_queue
from classes.worlds.world import World
import pygame
from pygame.sprite import Sprite


class Object(ABC, Sprite):
    """A projectile, specify a source y if the projectile is only supposed to hit on a certain y value, it will hit all
    except for its source_type"""

    game_id: str

    def __init__(self, x: int, y: int, world: World):
        super().__init__()
        self.is_dead = False
        self.frame = 0
        self.world = world
        self.has_collision = False
        self.rect = self.image.get_rect()
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.x, self.y = x, y
        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called when the projectile is created"""
        pass

    @abstractmethod
    def on_death(self):
        """Called when the projectile dies or is removed"""
        pass

    def destroy(self):
        """Removes the projectile from the world"""
        self.world.objects.remove(self)
        self.kill()

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the plant here"""
        pass

    def collides(self, rect: pygame.Rect) -> bool:
        """Returns whether it collides with the rectangle"""
        return self.rect.bottom == rect.bottom and self.rect.colliderect(rect)

    @property
    def image(self) -> pygame.Surface:
        return sprites[self.game_id][self.frame]

    @abstractmethod
    def on_damage(self, damage: float):
        """called when damaged, return amount of damage the object takes"""

    def damage(self, damage: float):
        """Does damage to the object and also calls on_death if it dies"""
        damage = self.on_damage(damage)
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
        update_queue.append(surface.blit(self.image, (self.x, self.y)))
