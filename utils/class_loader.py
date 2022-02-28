import os
import logging
from typing import Dict

classes: Dict[str, Dict[str, type]] = {}


def load_class(cls: type):
    """A decorator that when added to a class, it will add it to the class list"""
    game_id = cls.__name__.lower()
    class_type = cls.__base__.__name__.lower()
    if class_type not in classes:
        classes[class_type] = {}
    classes[class_type][game_id] = cls
    cls.game_id = game_id
    return cls


def load_classes():
    """Loads all of the classes"""
    for folder in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'classes')):
        for file in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'classes', folder)):
            try:
                if '.py' in file or '.pyw' in file:
                    name = '.'.join(
                        ('classes', folder, file)
                    ).replace('.py', '').replace('.pyw', '')
                    __import__(name)
            except Exception as e:
                logging.warning(e)


class ClassNameConflictError(Exception):
    """Class is already register"""
