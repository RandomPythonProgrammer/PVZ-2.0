import pygame
from typing import List

__cancelled = False
events: List[pygame.event.Event] = []


def set_cancelled(status: bool):
    global __cancelled
    __cancelled = status


def get_cancelled() -> bool:
    return __cancelled


def get_events():
    global events
    events.clear()
    events.extend(pygame.event.get())
