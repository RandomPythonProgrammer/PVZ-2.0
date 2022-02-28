import pygame
from typing import List

is_cancelled = False
events: List[pygame.event.Event] = []


def set_cancelled(status: bool):
    global is_cancelled
    is_cancelled = status


def get_events():
    global events
    events.clear()
    events.extend(pygame.event.get())
