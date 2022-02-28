import os
import logging
from typing import Dict

classes: Dict[str, Dict[str, type]] = {}


def load_class(class_type, game_id):
    def load(cls):
        if class_type not in classes:
            classes[class_type] = {}
        classes[class_type][game_id] = cls
        cls.game_id = game_id
    return load


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
    pass
