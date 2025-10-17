class Map:
    def __init__(self, cuao):
        self.matrix = None
        self.tiles = cuao
m = Map('cuaoo')
print(getattr(m, 'matrix', None))