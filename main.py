from utils.class_loader import classes
import os
import logging


def load_classes():
    for folder in os.listdir(os.path.join(os.path.dirname(__file__), 'classes')):
        for file in os.listdir(os.path.join(os.path.dirname(__file__), 'classes', folder)):
            try:
                if ('.py' in file or '.pyw' in file) and file[0] != '_':
                    name = '.'.join(
                        ('classes', folder, file)
                    ).replace('.py', '').replace('.pyw', '')
                    exec(f"from {name} import *")
            except Exception as e:
                logging.warning(e)


if __name__ == '__main__':
    load_classes()
    print(classes)
