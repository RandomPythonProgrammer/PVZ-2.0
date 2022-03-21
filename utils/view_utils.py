class ViewPort:
    """A viewport for relative rendering"""
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def project(self, x: float, y: float):
        """Gives the position relative to the viewport"""
        return x-self.x, y-self.y

    def unproject(self, x: float, y: float):
        """Gives the absolute position when given a relative"""
        return x+self.x, y+self.y
