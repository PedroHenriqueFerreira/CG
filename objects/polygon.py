from OpenGL.GL import *
from OpenGL.GLUT import *

from objects.texture import Texture2D

from utils.triangle import Triangle

from structures.vector import Vec2, Vec3

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

import numpy as np
import glm

class Polygon:
    def __init__(
        self,
        map: 'Map',
        coords: list[Vec2],
        height: float,
        color: Vec3,
        texture: Texture2D, 
        texture_size: float
    ):
        self.map = map
        
        self.coords = coords
        self.height = height
        self.color = color
        self.texture = texture
        self.texture_size = texture_size
        
        self.triangles: list[Vec3] = []
        self.colors: list[Vec3] = []
        self.normals: list[Vec3] = []
        self.tex_coords: list[Vec2] = []
        
        self.gl_list = 0
    
    def load(self):
        if len(self.triangles) > 0:
            return
        
        if self.is_clockwise():
            coords = self.coords[::-1]
        else:
            coords = self.coords[:]

        while len(coords) >= 3:
            triangle = self.get_ear(coords)
            
            if triangle is None:
                break
            
            p1 = triangle.p1
            p2 = triangle.p2
            p3 = triangle.p3
            
            self.tex_coords.extend([
                p1 / self.texture_size, 
                p2 / self.texture_size, 
                p3 / self.texture_size
            ])
            
            p1 = p1.to_vec3(self.height)
            p2 = p2.to_vec3(self.height)
            p3 = p3.to_vec3(self.height)
            
            self.triangles.extend([p1, p2, p3])
            
            self.normals.extend([Vec3(0, 0, 1)] * 3)
            self.colors.extend([self.color] * 3)

        t1 = Vec2(0, 0)
        
        for prev, curr in zip(self.coords[:-1], self.coords[1:]):
            vector = curr - prev
            
            normal = vector.normalize()
            length = vector.length()
            
            t2 = Vec2(length, 0) / self.texture_size
            t3 = Vec2(length, self.height) / self.texture_size
            t4 = Vec2(0, self.height) / self.texture_size
            
            self.tex_coords.extend([t1, t2, t3, t1, t3, t4])
            
            p1 = prev.to_vec3(0.00001)
            p2 = curr.to_vec3(0.00001)
            p3 = curr.to_vec3(self.height)
            p4 = prev.to_vec3(self.height)
            
            self.triangles.extend([p1, p2, p3, p1, p3, p4])

            self.normals.extend([Vec3(-normal.y, normal.x, 0)] * 6)
            self.colors.extend([self.color] * 6)

    def draw(self):
        if self.gl_list > 0:
            return glCallList(self.gl_list)
        
        self.load()
        self.texture.load()
        
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
        glBegin(GL_TRIANGLES)
        
        for p, c, n, t in zip(self.triangles, self.colors, self.normals, self.tex_coords):
            glNormal3f(n.x, n.y, n.z)
            glColor3f(c.x, c.y, c.z)
            glTexCoord2f(t.x, t.y)
            glVertex3f(p.x, p.y, p.z)
            
        glEnd()
        
        glBindTexture(GL_TEXTURE_2D, 0)
        glEndList()
            

    def is_clockwise(self):
        ''' Checa se as coordenadas estão no sentido horário '''
        
        coords = self.coords
        
        sum = (coords[0].x - coords[len(coords) - 1].x) * (coords[0].y + coords[len(coords) - 1].y)

        for i in range(len(coords) - 1):
            sum += (coords[i + 1].x - coords[i].x) * (coords[i + 1].y + coords[i].y)

        return sum > 0

    def get_ear(self, coord: list[Vec2]):
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

            tritest = False
            if triangle.is_convex():
                for x in coord:
                    if triangle.contains(x):
                        tritest = True

                if not tritest:
                    del coord[i % size]
                    return triangle
                
        return None