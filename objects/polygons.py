from typing import TYPE_CHECKING

from OpenGL.GL import * 

from numpy import ndarray, hstack, concatenate
from glm import vec2, vec3, normalize, length, mat4

from objects.vertex_arrays import DefaultVertexArray

if TYPE_CHECKING:
    from objects.map import Map

class Triangle:
    ''' Classe utilizada para armazenar operações com triângulos '''
    
    def __init__(self, p1: vec2, p2: vec2, p3: vec2):
        self.p1 = p1 # Ponto 1
        self.p2 = p2 # Ponto 2
        self.p3 = p3 # Ponto 3
        
    def values(self):
        ''' Retorna os pontos do triângulo '''
        
        return self.p1, self.p2, self.p3
        
    def is_convex(self):
        ''' Checa se o triângulo é convexo '''
        
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3

        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x) >= 0
    
    def contains(self, p: vec2):
        ''' Checa se o triângulo contém um ponto '''
        
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3
        
        if p in (p1, p2, p3):
            return False
        
        return (
            (p3.x - p.x) * (p1.y - p.y) - (p1.x - p.x) * (p3.y - p.y) >= 0 and
            (p1.x - p.x) * (p2.y - p.y) - (p2.x - p.x) * (p1.y - p.y) >= 0 and
            (p2.x - p.x) * (p3.y - p.y) - (p3.x - p.x) * (p2.y - p.y) >= 0
        )

class Polygon:
    ''' Classe utilizada para armazenar polígonos '''
    
    def __init__(self, app: 'Map', coords: list[vec2], height: float, texture_size: float):
        self.app = app # Instância do mapa
        
        self.coords = coords # Coordenadas do polígono
        
        self.height = app.metrics.from_meters(height) # Altura do polígono em METROS
        self.texture_size = app.metrics.from_meters(texture_size) # Tamanho da textura em METROS
        
        self.triangles = self.load() # Triângulos do polígono

    def get_data(self) -> ndarray:
        ''' Retorna os dados do polígono '''
    
        positions: list[vec3] = []
        normals: list[vec3] = []
        tex_coords: list[vec2] = []
        tangents: list[vec3] = []
        
        # Topo do polígono
        for point in self.triangles:
            positions.append(vec3(point, self.height))
            tex_coords.append(point / self.texture_size)
            
            normals.append(vec3(0, 0, 1))
            
        # Lados do polígono
        for prev, curr in zip(self.coords[:-1], self.coords[1:]):
            delta = curr - prev
            
            unit = normalize(delta)
            size = length(delta)
             
            t1 = vec2(0, 0) / self.texture_size
            t2 = vec2(size, 0) / self.texture_size
            t3 = vec2(size, self.height) / self.texture_size
            t4 = vec2(0, self.height) / self.texture_size
            
            p1 = vec3(prev, 0)
            p2 = vec3(curr, 0)
            p3 = vec3(curr, self.height)
            p4 = vec3(prev, self.height)
            
            n = vec3(-unit.y, unit.x, 0)
            
            positions.extend([p1, p2, p3, p1, p3, p4])
            normals.extend([n] * 6)
            tex_coords.extend([t1, t2, t3, t1, t3, t4])
        
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

        return hstack([positions, normals, tex_coords, tangents]).reshape(-1)
        
    def load(self):
        ''' Triangula o polígono '''
        
        triangles: list[vec2] = []
        
        if self.is_clockwise():
            coords = self.coords[::-1]
        else:
            coords = self.coords[:]

        while len(coords) >= 3:
            triangle = self.get_ear(coords)
            
            if triangle is None:
                break
            
            triangles.extend(triangle.values())
            
        return triangles
            
    def is_clockwise(self):
        ''' Checa se as coordenadas estão no sentido horário '''
        
        coords = self.coords
        
        sum = (coords[0].x - coords[len(coords) - 1].x) * (coords[0].y + coords[len(coords) - 1].y)

        for i in range(len(coords) - 1):
            sum += (coords[i + 1].x - coords[i].x) * (coords[i + 1].y + coords[i].y)

        return sum > 0

    def get_ear(self, coord: list[vec2]):
        ''' Retorna o triângulo que é uma orelha no polígono '''
        
        size = len(coord)

        if size < 3:
            return None

        if size == 3:
            triangle = Triangle(*coord)
            del coord[:]
            return triangle

        for i in range(size):
            triangle = Triangle(coord[(i - 1) % size], coord[i % size], coord[(i + 1) % size])

            if not triangle.is_convex():
                continue

            tritest = False
            
            for x in coord:
                if triangle.contains(x):
                    tritest = True
                    
                    break
            
            if tritest:
                continue

            del coord[i % size]
            return triangle
                
        return None

class Polygons:
    ''' Classe que armazena os polígonos do mapa '''
    
    def __init__(self, app: 'Map'):
        self.app = app
        
        self.grasses: list[Polygon] = []
        self.waters: list[Polygon] = []
        self.unknowns: list[Polygon] = []
        self.buildings: list[Polygon] = []
        
        self.grasses_vao: DefaultVertexArray | None = None
        self.waters_vao: DefaultVertexArray | None = None
        self.unknowns_vao: DefaultVertexArray | None = None
        self.buildings_vao: DefaultVertexArray | None = None
        
        self.identity = mat4(1)
    
    def draw(self):
        ''' Desenha os polígonos '''
        
        self.app.shaders.default.use()
        
        self.app.shaders.default.set('projection', self.app.projection.matrix)
        self.app.shaders.default.set('view', self.app.view.matrix)
        self.app.shaders.default.set('model', self.identity)
        
        self.app.shaders.default.set('lightPos', self.app.light.position)
        self.app.shaders.default.set('viewPos', self.app.view.position)
        
        if self.grasses_vao:
            self.app.textures.grass_diffuse.use(0)
            self.app.textures.grass_normal.use(1)
            self.app.textures.grass_displacement.use(2)
            
            self.app.shaders.default.set('diffuseMap', 0)
            self.app.shaders.default.set('normalMap', 1)
            self.app.shaders.default.set('displacementMap', 2)
            
            self.grasses_vao.draw()
            
            self.app.textures.grass_diffuse.unuse()
            self.app.textures.grass_normal.unuse()
            self.app.textures.grass_displacement.unuse()
            
        if self.waters_vao:
            self.app.textures.water_diffuse.use(0)
            self.app.textures.water_normal.use(1)
            self.app.textures.water_displacement.use(2)
            
            self.app.shaders.default.set('diffuseMap', 0)
            self.app.shaders.default.set('normalMap', 1)
            self.app.shaders.default.set('displacementMap', 2)
            
            self.waters_vao.draw()
            
            self.app.textures.water_diffuse.unuse()
            self.app.textures.water_normal.unuse()
            self.app.textures.water_displacement.unuse()
        
        if self.unknowns_vao:
            self.app.textures.unknown_diffuse.use(0)
            self.app.textures.unknown_normal.use(1)
            self.app.textures.unknown_displacement.use(2)
            
            self.app.shaders.default.set('diffuseMap', 0)
            self.app.shaders.default.set('normalMap', 1)
            self.app.shaders.default.set('displacementMap', 2)
            
            self.unknowns_vao.draw()
            
            self.app.textures.unknown_diffuse.unuse()
            self.app.textures.unknown_normal.unuse()
            self.app.textures.unknown_displacement.unuse()
            
        if self.buildings_vao:
            self.app.textures.building_diffuse.use(0)
            self.app.textures.building_normal.use(1)
            self.app.textures.building_displacement.use(2)
            
            self.app.shaders.default.set('diffuseMap', 0)
            self.app.shaders.default.set('normalMap', 1)
            self.app.shaders.default.set('displacementMap', 2)
            
            self.buildings_vao.draw()
            
            self.app.textures.building_diffuse.unuse()
            self.app.textures.building_normal.unuse()
            self.app.textures.building_displacement.unuse()

        self.app.shaders.default.unuse()
    
    def load(self, data: dict):
        for feature in data['features']:
            properties: dict = feature['properties']

            geometry_coords = feature['geometry']['coordinates']
            geometry_type = feature['geometry']['type']

            if geometry_type != 'Polygon':
                continue

            coords = [self.app.metrics.normalize(vec2(*coord)) for coord in geometry_coords[0]]

            self.load_polygon(properties, coords)
            
        water_data = concatenate([polygon.get_data() for polygon in self.waters])
        grass_data = concatenate([polygon.get_data() for polygon in self.grasses])
        building_data = concatenate([polygon.get_data() for polygon in self.buildings])
        unknown_data = concatenate([polygon.get_data() for polygon in self.unknowns])
        
        self.waters_vao = DefaultVertexArray(water_data)
        self.grasses_vao = DefaultVertexArray(grass_data)
        self.buildings_vao = DefaultVertexArray(building_data)
        self.unknowns_vao = DefaultVertexArray(unknown_data)
        
    def load_polygon(self, properties: dict, coords: list[vec2]):
        ''' Carrega um novo polígono '''
        
        if properties.get('type') in ('boundary', ):
            return

        # Verifica se o polígono é uma parte verde
        if (
            properties.get('landuse') in ('forest', 'allotments', 'meadow', 'grass') or 
            properties.get('natural') in ('grassland', 'heath', 'scrub', 'wood', 'wetland') or 
            properties.get('leisure') in ('park',)
        ):
            self.grasses.append(Polygon(self.app, coords, 0.1, 10))
        
        # Verifica se o polígono é uma parte de água
        elif (
            properties.get('leisure') in ('swimming_pool',) or 
            properties.get('natural') in ('water',)
        ):
            self.waters.append(Polygon(self.app, coords, 0.2, 5))

        # Verifica se o polígono é algo desconhecido
        elif (
            not properties.get('building')
        ):
            self.unknowns.append(Polygon(self.app, coords, 0.3, 10))
        
        # Verifica se o polígono é um prédio
        else:
            height = float(properties.get('height', '3'))
            
            self.buildings.append(Polygon(self.app, coords, height, 5))
