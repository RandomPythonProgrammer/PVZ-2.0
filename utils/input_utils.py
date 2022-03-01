import pygame
from typing import List

__cancelled = False
events: List[pygame.event.Event] = []


def set_cancelled(status: bool):
    """Sets whether the click event has been done"""
    global __cancelled
    __cancelled = status


def get_cancelled() -> bool:
    """Returns whether the click event has been done"""
    return __cancelled


def get_events():
    """Returns all of the events from this game loop"""
    global events
    events.clear()
    events.extend(pygame.event.get())
