from OpenGL.GL import *

from numpy import array
from ctypes import c_void_p

from structures.vector import Vec2, Vec3

class VAO:
    def __init__(self, coords: list[Vec3], colors: list[Vec3], normals: list[Vec3], tex_coords: list[Vec2], tangents: list[Vec3]):
        self.coords = coords
        self.colors = colors
        self.normals = normals
        self.tex_coords = tex_coords
        self.tangents = tangents
        
        self.id = self.load()
    
    def load(self):
        coords = array(self.coords, dtype='float32').reshape(-1)
        colors = array(self.colors, dtype='float32').reshape(-1)
        normals = array(self.normals, dtype='float32').reshape(-1)
        tex_coords = array(self.tex_coords, dtype='float32').reshape(-1)
        tangents = array(self.tangents, dtype='float32').reshape(-1)
        
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao) 

        vbo_coords = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_coords)
        glBufferData(GL_ARRAY_BUFFER, coords.nbytes, coords, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, c_void_p(0))
        glEnableVertexAttribArray(0)

        vbo_colors = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_colors)
        glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 12, c_void_p(0))
        glEnableVertexAttribArray(1)   
        
        vbo_normals = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 12, c_void_p(0))
        glEnableVertexAttribArray(2)
        
        vbo_tex_coords = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_tex_coords)
        glBufferData(GL_ARRAY_BUFFER, tex_coords.nbytes, tex_coords, GL_STATIC_DRAW)
        glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, 8, c_void_p(0))
        glEnableVertexAttribArray(3)

        vbo_tangents = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_tangents)
        glBufferData(GL_ARRAY_BUFFER, tangents.nbytes, tangents, GL_STATIC_DRAW)
        glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, 12, c_void_p(0))
        glEnableVertexAttribArray(4)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
        glBindVertexArray(0)
        
        return vao