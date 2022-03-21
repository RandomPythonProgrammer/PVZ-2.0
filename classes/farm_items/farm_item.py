from abc import ABC, abstractmethod
from classes.tiles.tile import Tile
from utils.asset_loader import sprites
from classes.worlds.world import World
import pygame
from pygame.sprite import Sprite


class FarmItem(ABC, Sprite):
    """A farm item"""

    game_id: str

    def __init__(self, x: int, y: int, tile: Tile, team: int, world: World):
        super().__init__()
        self.is_dead = False
        self.frame = 0
        self.cost = 0
        self.cooldown = 0
        self.visible = True
        self.health = -1
        self.tile = tile
        self.world = world
        self.rect = self.image.get_rect()
        self.rect.update(x, y, self.rect.width, self.rect.height)
        self.x, self.y = x, y
        self.team = team
        self.has_collision = True
        self.on_create()

    @abstractmethod
    def on_create(self):
        """Called when the farm item is created"""

    @abstractmethod
    def on_death(self):
        """Called when the farm item dies or is removed"""

    def destroy(self):
        """Removes the farm item from the world"""
        self.world.farm_items.remove(self)
        self.kill()

    @classmethod
    @abstractmethod
    def can_place(cls, tile: Tile, world: World) -> bool:
        """Returns weather the farm item can be farm item or not"""

    @abstractmethod
    def update(self, dt: float):
        """Called every frame, or whenever the world calls it, write the actions of the farm item here"""

    @abstractmethod
    def on_damage(self, damage: float, source: type) -> float:
        """Called when zombie is damaged, return the amount of damage the zombie takes"""

    def damage(self, damage: float, source: type):
        """Does damage to the farm item and also calls on_death if it dies"""
        self.health -= self.on_damage(damage, source)
        if self.health <= 0:
            self.is_dead = True
            self.on_death()

    def collides(self, sprite: pygame.sprite.Sprite) -> bool:
        """Returns whether the farm item collides with a sprite"""
        return abs(self.rect.bottom - sprite.rect.bottom) < self.world.tile_size \
               and pygame.sprite.collide_mask(self, sprite)

    @property
    def image(self) -> pygame.Surface:
        return sprites[self.game_id][self.frame]

    def render(self, surface: pygame.Surface):
        if not self.visible:
            return
        if self.team == 1:
            surface.blit(self.image, (self.x, self.y))
        elif self.team == 2:
            surface.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
