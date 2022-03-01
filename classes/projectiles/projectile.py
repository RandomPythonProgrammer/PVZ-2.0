from abc import ABC, abstractmethod
from utils.asset_loader import sprites
from classes.worlds.world import World
import pygame
from pygame.sprite import Sprite
from classes.plants.plant import Plant
from classes.zombies.zombie import Zombie


class Projectile (ABC, Sprite):
    """A projectile, specify a source y if the projectile is only supposed to hit on a certain y value, it will hit all
    except for its source_type"""

    game_id: str

    def __init__(self, x: int, y: int, world: World, velocity: tuple, source_y=None, source_type=Plant):
        super().__init__()
        self.is_dead = False
        self.frame = 0
        self.damage = 0
        self.velocity = velocity
        self.source_y = source_y
        self.visible = True
        self.world = world
        self.source_type = source_type
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
        self.world.projectiles.remove(self)
        self.kill()

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the plant here"""
        pass

    def get_collisions(self) -> list:
        """Returns a list of colliding objects based on rules"""
        objects = []

        objects.extend([object for object in self.world.objects
                        if (object.has_collision and (self.source_y is None or abs(self.source_y - object.rect.bottom) < self.world.tile_size))
                        and object.rect.colliderect(self.rect)
                        and pygame.sprite.collide_mask(self, object)])

        if self.source_type != Plant:
           objects.extend([plant for plant in self.world.plants
                           if (self.source_y is None or abs(self.source_y - plant.rect.bottom) < self.world.tile_size)
                           and plant.rect.colliderect(self.rect)
                           and pygame.sprite.collide_mask(self, plant)])

        if self.source_type != Zombie:
            objects.extend([zombie for zombie in self.world.zombies
                            if (self.source_y is None or abs(self.source_y - zombie.rect.bottom) < self.world.tile_size)
                            and zombie.rect.colliderect(self.rect)
                            and pygame.sprite.collide_mask(self, zombie)])

        return objects

    @property
    def image(self) -> pygame.Surface:
        return sprites[self.game_id][self.frame]

    def move(self, x, y):
        """Moves the projectile"""
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)

    def render(self, surface: pygame.Surface):
        if not self.visible:
            return
        surface.blit(self.image, (self.x, self.y))
