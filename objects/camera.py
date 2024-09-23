from OpenGL.GLU import *

class Camera2:
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
    
from glm import vec3, lookAt, perspective, radians

from numpy import array
        
class Camera:
    def __init__(self, position: vec3, target: vec3, up: vec3):
        self.position = position
        self.target = target
        self.up = up
        
        self.matrix = self.get_matrix()
    
    def update(self, position: vec3, target: vec3, up: vec3):
        self.position = position
        self.target = target
        self.up = up
        
        self.matrix = self.get_matrix()
        
    def get_matrix(self):
        return array(lookAt(self.position, self.target, self.up)).T
        
class Projection:
    def __init__(self, fov: float, aspect: float, near: float, far: float):
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        
        self.matrix = self.get_matrix()
        
    def update(self, aspect: float):
        self.aspect = aspect
        
        self.matrix = self.get_matrix()

    def get_matrix(self):
        return array(perspective(radians(self.fov), self.aspect, self.near, self.far)).T
