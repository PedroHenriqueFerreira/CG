from typing import TYPE_CHECKING

from glm import vec2, vec3, mat2, rotate, radians, normalize, dot, mat4
from numpy import hstack, concatenate, ndarray

from objects.vertex_arrays import DefaultVertexArray

from settings import *

if TYPE_CHECKING:
    from objects.map import Map

class Circle:
    ''' Classe que representa um círculo. '''
    
    def __init__(self, pos: vec2, size: float, height: float, texture_size: float):
        self.pos = pos # Posição
        self.size = size # Tamanho
        self.height = height # Altura
        self.texture_size = texture_size # Tamanho da textura
    
        self.triangles = self.load() # Triângulos
    
    def get_data(self) -> ndarray:
        ''' Retorna os dados do círculo. '''
        
        positions: list[vec3] = []
        normals: list[vec3] = []
        tex_coords: list[vec2] = []
        tangents: list[vec3] = []
        
        for point in self.triangles:
            positions.append(vec3(point, self.height))
            normals.append(vec3(0, 0, 1))
            tex_coords.append(point / self.texture_size)
            tangents.append(vec3(1, 0, 0))

        return hstack([positions, normals, tex_coords, tangents]).reshape(-1)
    
    def load(self):
        ''' Carrega o círculo. '''
        
        segments = 30
        
        triangles: list[vec2] = []
        
        step = 360 / segments
        
        origin = vec2(self.size / 2, 0)
        
        axis = vec3(0, 0, 1)
        
        for i in range(segments + 1):
            curr_rotation = rotate(radians(i * step), axis)
            next_rotation = rotate(radians((i + 1) * step), axis)
            
            triangles.append(self.pos)
            triangles.append(mat2(curr_rotation) * origin + self.pos)
            triangles.append(mat2(next_rotation) * origin + self.pos)
            
        return triangles

class LineString:
    ''' Classe que representa as linhas que compõem o mapa. '''
    
    def __init__(self, app: 'Map', coords: list[vec2], size: float, height: float, texture_size: float):
        self.coords = coords # Coordenadas
        self.size = app.metrics.from_meters(size) # Largura da linha em METROS
        self.height = app.metrics.from_meters(height) # Altura da linha em METROS
        self.texture_size = texture_size # Tamanho da textura
        
        self.initial_circle = Circle(coords[0], self.size, self.height, texture_size) # Círculo inicial
        self.final_circle = Circle(coords[-1], self.size, self.height, texture_size) # Círculo final
        
        self.triangles = self.load() # Triângulos

    def get_data(self) -> ndarray:
        ''' Retorna os dados da linha. '''
    
        positions: list[vec3] = []
        normals: list[vec3] = []
        tex_coords: list[vec2] = []
        tangents: list[vec3] = []
        
        for point in self.triangles:
            positions.append(vec3(point, self.height))
            normals.append(vec3(0, 0, 1))
            tex_coords.append(point / self.texture_size)
            tangents.append(vec3(1, 0, 0))

        initial_circle_data = self.initial_circle.get_data()
        data = hstack([positions, normals, tex_coords, tangents]).reshape(-1)
        final_circle_data = self.final_circle.get_data()
        
        return concatenate([initial_circle_data, data, final_circle_data])
        
    def load(self):
        ''' Carrega a linha. '''
        
        size = self.size / 2
        
        pairs: list[tuple[vec2, vec2]] = []
        
        for prev, curr, next in zip([None] + self.coords[:-1], self.coords, self.coords[1:] + [None]):
            t0 = vec2(0, 0) if prev is None else normalize(curr - prev)
            t1 = vec2(0, 0) if next is None else normalize(next - curr)

            n0 = vec2(-t0.y, t0.x)
            n1 = vec2(-t1.y, t1.x)

            if prev is None:
                pairs.append((curr + n1 * size, curr - n1 * size))

            elif next is None:
                pairs.append((curr + n0 * size, curr - n0 * size))

            else:
                m = normalize(n0 + n1)

                dy = size / dot(m, n1)

                pairs.append((curr + m * dy, curr - m * dy))

        # Transformando os pares em triângulos
        
        triangles: list[vec2] = []
        
        for prev, curr in zip(pairs[:-1], pairs[1:]):
            p1 = prev[0]
            p2 = prev[1]
            p3 = curr[1]
            p4 = curr[0]
            
            triangles.extend([p1, p2, p3, p1, p3, p4])

        return triangles
        
class LineStrings:
    def __init__(self, app: 'Map'):
        self.app = app
        
        self.roads: list[LineString] = []
        self.path: LineString | None = None
        
        self.roads_vao: DefaultVertexArray | None = None
        
        self.identity = mat4(1.0) # Matriz identidade
        
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
        
        if self.roads_vao:
            self.app.textures.road_diffuse.use(0)
            self.app.textures.road_normal.use(1)
            
            self.app.shaders.default.set('diffuse', 0)
            self.app.shaders.default.set('normal', 1)
            
            self.app.shaders.default.set('material.ambient', self.app.materials.road.ambient)
            self.app.shaders.default.set('material.diffuse', self.app.materials.road.diffuse)
            self.app.shaders.default.set('material.specular', self.app.materials.road.specular)
            self.app.shaders.default.set('material.shininess', self.app.materials.road.shininess)
            
            self.roads_vao.draw()
            
            self.app.textures.road_diffuse.unuse()
            self.app.textures.road_normal.unuse()

        if self.path:
            self.app.textures.path_diffuse.use(0)
            self.app.textures.path_normal.use(1)
            
            self.app.shaders.default.set('diffuse', 0)
            self.app.shaders.default.set('normal', 1)
            
            self.app.shaders.default.set('material.ambient', self.app.materials.path.ambient)
            self.app.shaders.default.set('material.diffuse', self.app.materials.path.diffuse)
            self.app.shaders.default.set('material.specular', self.app.materials.path.specular)
            self.app.shaders.default.set('material.shininess', self.app.materials.path.shininess)
            
            DefaultVertexArray(self.path.get_data()).draw()
            
            self.app.textures.path_diffuse.unuse()
            self.app.textures.path_normal.unuse()

        self.app.shaders.default.unuse()
        
    def load(self, data: dict):
        for feature in data['features']:
            properties: dict = feature['properties']

            geometry_coords = feature['geometry']['coordinates']
            geometry_type = feature['geometry']['type']

            if geometry_type != 'LineString':
                continue

            coords = [self.app.metrics.normalize(vec2(*coord)) for coord in geometry_coords]

            self.load_road(properties, coords)
            
        roads_data = concatenate([road.get_data() for road in self.roads])
        
        self.roads_vao = DefaultVertexArray(roads_data)
            
    def load_road(self, properties: dict, coords: list[vec2]):
        if properties.get('highway') not in (
            'motorway', 'motorway_link', 'trunk',
            'trunk_link', 'primary', 'primary_link',

            'secondary', 'secondary_link', 'tertiary',
            'tertiary_link', 'road',

            'living_street', 'pedestrian', 'unclassified',
            'residential',
        ):
            return

        self.roads.append(LineString(self.app, coords, ROAD_SIZE, 0.4, 1))
        
    def load_path(self, path: list[vec2]):
        self.path = LineString(self.app, path, PATH_SIZE, 0.5, 1)