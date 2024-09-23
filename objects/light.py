from numpy import array
from glm import vec3, lookAt

class Light:
    def __init__(
        self, 
        position: vec3, 
        Ia: vec3, 
        Id: vec3,
        Is: vec3
    ):
        self.position = position
        
        self.Ia = Ia
        self.Id = Id
        self.Is = Is
        
        self.direction = vec3(0, 0, 0)
        self.up = vec3(0, 1, 0)
        
        self.matrix = self.get_matrix()
    
    def update(self, position: vec3):
        self.position = position
        
        self.matrix = self.get_matrix()
         
    def get_matrix(self):
        return array(lookAt(self.position, self.direction, self.up)).T