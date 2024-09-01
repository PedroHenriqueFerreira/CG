from OpenGL.GLU import *

class Camera:
    def __init__(self, speed: float, animated: bool):
        self.speed = speed
        self.animate = animated
        
        self.values: list[float] | None = None
        
        
    def update(self, *values: float):
        if not self.values or not self.animate:
            self.values = list(values)
        else:
            for i, value in enumerate(values):
                self.values[i] = self.values[i] * (1 - self.speed) + values[i] * self.speed
                
        gluLookAt(*self.values)