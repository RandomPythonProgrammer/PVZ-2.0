import os
import logging
import pygame
from typing import Dict

sprites: Dict[str, pygame.Surface] = {}


def load_sprites():
    """Loads all of the assets into the game"""
    for folder in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'assets')):
        for file in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'assets', folder)):
            try:
                path = os.path.join(os.path.dirname(__file__), '..', 'assets', folder, file)
                img = pygame.image.load(path).convert_alpha()
                if folder not in sprites:
                    sprites[folder] = []
                sprites[folder].append(img)
            except Exception as e:
                logging.warning(e)
