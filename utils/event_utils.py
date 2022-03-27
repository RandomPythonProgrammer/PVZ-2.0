from abc import ABC
import time


class Event(ABC):
    """Base event class"""
    def __init__(self, team: int):
        self.team = team
        self.time = time.time()


class ClickEvent(Event):
    """Called when an object is clicked on"""
    def __init__(self, team: int, clicked: object):
        super(ClickEvent, self).__init__(team)
        self.clicked = clicked


class PlaceEvent(Event):
    """Called when an object is placed"""
    def __init__(self, team: int, placed: object, x: int, y: int, tile: object):
        super(PlaceEvent, self).__init__(team)
        self.placed = placed
        self.tile = tile
        self.x, self.y = x, y


class DestroyEvent(Event):
    """Called when an object is destroyed"""
    def __init__(self, team: int, destroyed: object):
        super(DestroyEvent, self).__init__(team)
        self.destroyed = destroyed


class CommandIssued(Event):
    """Called when a command is issued to the server"""
    def __init__(self, team: int, command: str):
        super(CommandIssued, self).__init__(team)
        self.command = command


class PlayerConnectEvent(Event):
    """When player joins"""


class PlayerDisconnectEvent(Event):
    """When player leaves"""
