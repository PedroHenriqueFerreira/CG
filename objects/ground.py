from typing import TYPE_CHECKING
from OpenGL.GL import *

from glm import vec3, vec2, mat4
from numpy import hstack

from objects.vertex_arrays import DefaultVertexArray

if TYPE_CHECKING:
    from objects.map import Map

class Ground:
    def __init__(self, app: 'Map', texture_size: int = 10):
        self.app = app
        
        self.texture_size = self.app.metrics.from_meters(texture_size) # Tamanho da textura em METROS
        
        self.vao: DefaultVertexArray | None = None
        
        self.load()
        
    def load(self):
        p1 = vec3(-1.0, -1.0, -0.00001)
        p2 = vec3( 1.0, -1.0, -0.00001)
        p3 = vec3( 1.0,  1.0, -0.00001)
        p4 = vec3(-1.0,  1.0, -0.00001)
        
        t1 = vec2(p1) / self.texture_size
        t2 = vec2(p2) / self.texture_size
        t3 = vec2(p3) / self.texture_size
        t4 = vec2(p4) / self.texture_size
        
        positions = [p1, p2, p3, p1, p3, p4]
        normals = [vec3(0.0, 0.0, 1.0)] * 6
        tex_coords = [t1, t2, t3, t1, t3, t4]
        tangents: list[vec3] = []
        
        # Tangentes
        for i in range(0, len(positions), 3):
            v0 = positions[i]
            v1 = positions[i + 1]
            v2 = positions[i + 2]
            
            uv0 = tex_coords[i]
            uv1 = tex_coords[i + 1]
            uv2 = tex_coords[i + 2]
            
            delta_v1 = v1 - v0
            delta_v2 = v2 - v0
            
            delta_uv1 = uv1 - uv0
            delta_uv2 = uv2 - uv0
            
            try:
                f = 1.0 / (delta_uv1.x * delta_uv2.y - delta_uv1.y * delta_uv2.x)
                tangent = f * (delta_uv2.y * delta_v1 - delta_uv1.y * delta_v2)
            except:
                tangent = vec3(1, 0, 0)
            
            tangents.extend([tangent] * 3)
        
        data = hstack([positions, normals, tex_coords, tangents]).reshape(-1)
        
        self.vao = DefaultVertexArray(data)
        
        self.identity = mat4(1.0)
        
    def draw(self):
        self.app.shaders.default.use()
        
        self.app.shaders.default.set('projection', self.app.projection.matrix)
        self.app.shaders.default.set('view', self.app.view.matrix)
        self.app.shaders.default.set('model', self.identity)
        
        self.app.shaders.default.set('lightPos', self.app.light.position)
        self.app.shaders.default.set('viewPos', self.app.view.position)
        
        self.app.shaders.default.set('light.ambient', self.app.light.ambient)
        self.app.shaders.default.set('light.diffuse', self.app.light.diffuse)
        self.app.shaders.default.set('light.specular', self.app.light.specular)
        
        self.app.textures.ground_diffuse.use(0)
        self.app.textures.ground_normal.use(1)
        
        self.app.shaders.default.set('diffuse', 0)
        self.app.shaders.default.set('normal', 1)
        
        self.app.shaders.default.set('material.ambient', self.app.materials.ground.ambient)
        self.app.shaders.default.set('material.diffuse', self.app.materials.ground.diffuse)
        self.app.shaders.default.set('material.specular', self.app.materials.ground.specular)
        self.app.shaders.default.set('material.shininess', self.app.materials.ground.shininess)
        
        self.vao.draw()
        
        self.app.textures.ground_diffuse.unuse()