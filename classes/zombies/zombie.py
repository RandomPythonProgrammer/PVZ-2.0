from __future__ import annotations
from abc import ABC, abstractmethod
from utils.asset_loader import sprites
from utils.display_utils import update_queue
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.worlds.world import World


class Zombie (ABC, Sprite):
    """A zombie"""

    game_id: str

    def __init__(self, x: int, y: int, world: World):
        super().__init__()
        self.is_dead = False
        self.frame = 0
        self.health = -1
        self.world = world
        self.rect = self.image.get_rect()
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.x, self.y = x, y
        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called when the zombie is created"""
        pass

    @abstractmethod
    def on_death(self):
        """Called when the zombie dies or is removed"""
        pass

    def destroy(self):
        """Removes the zombie from the world"""
        self.world.zombies.remove(self)
        self.kill()

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the zombie here"""
        pass

    @abstractmethod
    def on_damage(self, damage: float) -> float:
        """Called when zombie is damaged, return the amount of damage the zombie takes"""
        pass

    def damage(self, damage: float):
        """Does damage to the zombie and also calls on_death if it dies"""
        damage = self.on_damage(damage)
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True
            self.on_death()

    @property
    def image(self) -> pygame.Surface:
        return sprites[self.game_id][self.frame]

    def move(self, x, y):
        """Moves the zombie"""
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)

    def render(self, surface: pygame.Surface):
        update_queue.append(surface.blit(self.image, (self.x, self.y)))
