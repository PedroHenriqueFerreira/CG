from glm import perspective, radians

class Projection:
    ''' Classe para armazenar informações sobre a projeção. '''
    
    def __init__(self, fov = 90.0, aspect = 1.0, near = 0.000001, far = 1000):
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        
        self.matrix = self.get_matrix()
        
    def update(self, aspect: float):
        self.aspect = aspect
        
        self.matrix = self.get_matrix()

    def get_matrix(self):
        return perspective(radians(self.fov), self.aspect, self.near, self.far)