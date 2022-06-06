from abc import ABC, abstractmethod
import time


_events = []


def get_events():
    global _events
    _events = [event for event in _events if not event.canceled]
    return _events


class Event(ABC):

    def __init__(self, origin):
        self.origin = origin
        self.time = time.time()
        self.canceled = False

    @abstractmethod
    def print(self):
        """Print what the event is"""
