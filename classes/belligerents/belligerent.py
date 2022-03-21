from __future__ import annotations
from abc import ABC, abstractmethod
from utils.asset_loader import sprites
import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.worlds.world import World


class Belligerent (ABC, Sprite):
    """A zombie"""

    game_id: str

    def __init__(self, x: int, y: int, team: int, world: World):
        super().__init__()
        self.is_dead = False
        self.visible = True
        self.frame = 0
        self.health = -1
        self.world = world
        self.team = team
        self.rect = self.image.get_rect()
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.x, self.y = x, y
        self.has_collision = True
        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called when the belligerent is created"""

    @abstractmethod
    def on_death(self):
        """Called when the belligerent dies or is removed"""

    def destroy(self):
        """Removes the belligerent from the world"""
        self.world.belligerents.remove(self)
        self.kill()

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the belligerent here"""

    @abstractmethod
    def on_damage(self, damage: float, source: type) -> float:
        """Called when belligerent is damaged, return the amount of damage the belligerent takes"""

    def damage(self, damage: float, source: type):
        """Does damage to the belligerent and also calls on_death if it dies"""
        damage = self.on_damage(damage, source)
        self.health -= damage
        if self.health <= 0:
            self.is_dead = True
            self.on_death()

    @property
    def image(self) -> pygame.Surface:
        return sprites[self.game_id][self.frame]

    def move(self, x, y):
        """Moves the belligerent"""
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)

    def render(self, surface: pygame.Surface):
        if not self.visible:
            return
        if self.team == 1:
            surface.blit(self.image, (self.x, self.y))
        elif self.team == 2:
            surface.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
