from glm import vec3
from numpy import array

from OpenGL.GL import *

from objects.vertex_arrays import SkyBoxVertexArray

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

class SkyBox:
    ''' Classe que representa o skybox. '''
    
    def __init__(self, app: 'Map'):
        self.app = app
        
        self.vao: SkyBoxVertexArray | None = None
        
        self.load()
        
    def load(self):
        ''' Carrega o skybox. '''
        
        positions = [
            # Baixo
            vec3(-1.0,  1.0, -1.0),
            vec3(-1.0, -1.0, -1.0),
            vec3( 1.0, -1.0, -1.0),
            vec3( 1.0, -1.0, -1.0),
            vec3( 1.0,  1.0, -1.0),
            vec3(-1.0,  1.0, -1.0),

            # Esquerda
            vec3(-1.0, -1.0,  1.0),
            vec3(-1.0, -1.0, -1.0),
            vec3(-1.0,  1.0, -1.0),
            vec3(-1.0,  1.0, -1.0),
            vec3(-1.0,  1.0,  1.0),
            vec3(-1.0, -1.0,  1.0),

            # Direita
            vec3(1.0, -1.0, -1.0),
            vec3(1.0, -1.0,  1.0),
            vec3(1.0,  1.0,  1.0),
            vec3(1.0,  1.0,  1.0),
            vec3(1.0,  1.0, -1.0),
            vec3(1.0, -1.0, -1.0),

            # Cima
            vec3(-1.0, -1.0,  1.0),
            vec3(-1.0,  1.0,  1.0),
            vec3( 1.0,  1.0,  1.0),
            vec3( 1.0,  1.0,  1.0),
            vec3( 1.0, -1.0,  1.0),
            vec3(-1.0, -1.0,  1.0),

            # Frente
            vec3(-1.0,  1.0, -1.0),
            vec3( 1.0,  1.0, -1.0),
            vec3( 1.0,  1.0,  1.0),
            vec3( 1.0,  1.0,  1.0),
            vec3(-1.0,  1.0,  1.0),
            vec3(-1.0,  1.0, -1.0),

            # Atrás
            vec3(-1.0, -1.0, -1.0),
            vec3(-1.0, -1.0,  1.0),
            vec3( 1.0, -1.0, -1.0),
            vec3( 1.0, -1.0, -1.0),
            vec3(-1.0, -1.0,  1.0),
            vec3( 1.0, -1.0,  1.0),
        ]
        
        data = array(positions).reshape(-1)
        
        self.vao = SkyBoxVertexArray(data)
        
    def draw(self):
        ''' Desenha o skybox. '''
        
        self.app.shaders.skybox.use()
        self.app.textures.skybox.use(0)
        
        self.app.shaders.skybox.set('view', self.app.view.matrix)
        self.app.shaders.skybox.set('projection', self.app.projection.matrix)
        self.app.shaders.skybox.set('skybox', 0)
        
        self.vao.draw()
        
        self.app.textures.skybox.unuse()
        self.app.shaders.skybox.unuse()
        
        