classes = {
    'zombies': [],
    'plants': [],
    'tiles': [],
    'worlds': []
}


def load_class(class_type):
    def load(cls):
        classes[class_type].append(cls)
    return load
