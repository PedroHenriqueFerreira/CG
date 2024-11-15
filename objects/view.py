from OpenGL.GLU import *

from glm import vec3, lookAt
        
class View:
    ''' Classe para armazenar informações sobre a câmera. '''
    
    def __init__(
        self, 
        position = vec3(0, 0, 1), 
        target = vec3(0, 0, 0), 
        up = vec3(0, 1, 0), 
        smoothness = 1
    ):
        self.position = position
        self.target = target
        self.up = up
        
        self.smoothness = smoothness
        
        self.matrix = self.get_matrix()
    
    def update(self, position: vec3, target: vec3, up: vec3):
        self.position = self.position + (position - self.position) * self.smoothness
        self.target = self.target + (target - self.target) * self.smoothness
        self.up = self.up + (up - self.up) * self.smoothness
        
        self.matrix = self.get_matrix()
        
    def get_matrix(self):
        return lookAt(self.position, self.target, self.up)
    
