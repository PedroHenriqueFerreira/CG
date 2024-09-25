from glm import vec3
        
class Light:
    ''' Classe para armazenar informações sobre a luz. '''
    
    def __init__(
        self, 
        position = vec3(0, 0, 1), 
        ambient = vec3(0.2, 0.2, 0.2),
        diffuse = vec3(1, 1, 1),
        specular = vec3(1, 1, 1)
    ):
        self.position = position
        
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
    
    def update(self, position: vec3):
        self.position = position
         