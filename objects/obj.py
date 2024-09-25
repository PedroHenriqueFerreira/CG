from OpenGL.GL import *

from os import path
from structures.vector import Vec2, Vec3

from objects.textures import Texture2D

class OBJ:
    def __init__(self, pathname: str):
        self.pathname = pathname
        
        self.vertices: list[Vec3] = []
        self.normals: list[Vec3] = []
        self.texcoords: list[Vec2] = []
        
        self.mtl: dict[str, list[float]] = {}
        
        self.faces: list[tuple[list[int], list[int], list[int], str]] = []
        
        self.loaded = False
        self.gl_list = 0
        
    def load(self):
        material: str | None = None
        
        with open(self.pathname, 'r', encoding='utf8') as f:
            data = f.readlines()
            
        for line in data:
            if line.startswith('#'): 
                continue
            
            values = line.split()
            
            if not values: 
                continue
            
            match values[0]:
                case 'v':
                    values = map(float, values[1:4])
        
                    self.vertices.append(Vec3(*values))
                case 'vn':
                    values = map(float, values[1:4])
                    
                    self.normals.append(Vec3(*values))
                case 'vt':
                    values = map(float, values[1:3])
                    
                    self.texcoords.append(Vec2(*values))
                case 'mtllib':
                    pathname = path.join(path.dirname(self.pathname), values[1])
                    
                    self.mtl = self.load_mtl(pathname)
        
                case 'usemtl' | 'usemat':
                    material = values[1]
                    
                case 'f':
                    vertices: list[int] = []
                    normals: list[int] = []
                    texcoords: list[int] = []
                    
                    for value in values[1:]:
                        elements = value.split('/')
                        
                        vertices.append(int(elements[0]))
                        
                        if len(elements) >= 2 and len(elements[1]) > 0:
                            texcoords.append(int(elements[1]))
                        else:
                            texcoords.append(0)
                            
                        if len(elements) >= 3 and len(elements[2]) > 0:
                            normals.append(int(elements[2]))
                        else:
                            normals.append(0)
                    
                    self.faces.append((vertices, normals, texcoords, material))
        
        self.loaded = True
        
    def load_mtl(self, pathname: str):
        dirname = path.dirname(pathname)
        
        mtl: dict[str, dict] = {}
        current: dict | None = None
        
        with open(pathname, 'r', encoding='utf8') as f:
            data = f.readlines()
            
        for line in data:
            if line.startswith('#'): 
                continue
            
            values = line.split()
            
            if not values: 
                continue
            
            match values[0]:
                case 'newmtl':
                    current = {}
                    
                    mtl[values[1]] = current
                    
                case 'map_Kd':
                    if current is None:
                        raise ValueError()
                    
                    current[values[0]] = values[1]
                    
                    imagefile = path.join(dirname, current['map_Kd'])
                    
                    current['texture_Kd'] = Texture2D(imagefile)
           
                case _:
                    if current is None:
                        raise ValueError()
                    
                    if len(values) == 4:
                        values.append('1.0')
                    
                    current[values[0]] = list(map(float, values[1:]))
           
        return mtl
                         
    def draw(self):
        if not self.loaded:
            self.load()

        default_material = {
            'diffuse': [0.8, 0.8, 0.8, 1.0],
            'ambient': [0.2, 0.2, 0.2, 1.0],
            'specular': [0.0, 0.0, 0.0, 1.0],
            'shininess': 0.0
        }
            
        if self.gl_list > 0:
            glCallList(self.gl_list)
        else:
            self.gl_list = glGenLists(1)
            
            glNewList(self.gl_list, GL_COMPILE)
            
            for face in self.faces:
                vertices, normals, texture_coords, material = face
                
                if material is not None:
                    mtl = self.mtl[material]
                    
                    if 'texture_Kd' in mtl:
                        mtl['texture_Kd'].load()
                        
                        glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'].id)
                    else:
                        glColor4f(*mtl['Kd'])
                        
                    # Load material
                    
                    # print(mtl)
                    
                    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, tuple(mtl['Ka']))
                    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, tuple(mtl['Kd']))
                    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, tuple(mtl['Ks']))
                    
                    # print('ULTIMO', mtl['Ns'][0])
                    
                    # glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mtl['Ns'][0])
                        
                glBegin(GL_POLYGON)
                
                for i in range(len(vertices)):
                    normal = self.normals[normals[i] - 1]
                    
                    glNormal3f(normal.x, normal.y, normal.z)
                        
                    if texture_coords[i] > 0:
                        texture = self.texcoords[texture_coords[i] - 1]
                        
                        glTexCoord2f(texture.x, texture.y)
                        
                    vertex = self.vertices[vertices[i] - 1]
                        
                    glVertex3f(vertex.x, vertex.y, vertex.z)
                
                glEnd()
                
            glBindTexture(GL_TEXTURE_2D, 0)
            glEndList()
            
    def free(self):
        glDeleteLists([self.gl_list])