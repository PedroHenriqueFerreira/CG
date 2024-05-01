from structures.vector import Vec2

class Camera:
    def __init__(self):
        self.values: list[float] | None = None
        
    def update(self, values: list[float]):
        if self.values is None:
            self.values = values
        else:
            for i, value in enumerate(values):
                self.values[i] = self.values[i] * 0.9 + value * 0.1