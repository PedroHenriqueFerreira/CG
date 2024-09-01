from OpenGL.GL import *
from OpenGL.GLUT import *

from typing import TYPE_CHECKING

from objects.texture import Texture2D

if TYPE_CHECKING:
    from objects.map import Map

from structures.vector import Vec2

from objects.color import Color

class Polygon:
    def __init__(self, map: 'Map', coords: list[Vec2], height: float, color: Color):
        self.map = map
        self.coords = coords
        self.height = height
        self.color = color
        
        self.triangles: list[Vec2] = []
        
        self.loaded = False
        
        self.gl_list = 0
        
        self.meter = self.map.km_to_world(0.001)
    
    def load(self):
        if len(self.triangles) > 0:
            return
        
        if self.is_clockwise(self.coords):
            coords = self.coords[::-1]
        else:
            coords = self.coords[:]

        while len(coords) >= 3:
            a = self.get_ear(coords)
            if a == []:
                break

            self.triangles.extend(a)

    def draw(self, texture: Texture2D):
        self.load()
            
        texture.load()
            
        if self.gl_list > 0:
            glCallList(self.gl_list)
        else:
            self.gl_list = glGenLists(1)
        
            glNewList(self.gl_list, GL_COMPILE)
            
            glColor3f(self.color.r, self.color.g, self.color.b)
            
            glBindTexture(GL_TEXTURE_2D, texture.id)
            glBegin(GL_TRIANGLES)
            
            min_ = Vec2.min(*self.triangles)
            max_ = Vec2.max(*self.triangles)
            width_ = max_.x - min_.x
            height_ = max_.y - min_.y
            
            glNormal3f(0, 0, 1)
            
            for point in self.triangles:
                x_ = (point.x - min_.x) / width_
                y_ = (point.y - min_.y) / height_
                
                glTexCoord2f(x_, y_)
                glVertex3f(point.x, point.y, self.meter * self.height)
                
            glEnd()
            
            if self.height == 0:
                glBindTexture(GL_TEXTURE_2D, 0)
                glEndList()
                return
            
            glBegin(GL_QUADS)
            
            for prev, curr in zip(self.coords[:-1], self.coords[1:]):
                dist = Vec2.distance(curr, prev)
                height = self.meter * self.height
                
                width_is_max = dist > height
                
                d = (curr - prev).normalize()
                
                glNormal3f(-d.y, d.x, 0)
                
                if width_is_max:
                    p = height / dist
                    
                    glTexCoord2f(0, 0)
                    glVertex3f(prev.x, prev.y, 0)
                    glTexCoord2f(1, 0)
                    glVertex3f(curr.x, curr.y, 0)
                    glTexCoord2f(1, p)
                    glVertex3f(curr.x, curr.y, height)
                    glTexCoord2f(0, p)
                    glVertex3f(prev.x, prev.y, height)
                else:
                    p = dist / height
                    
                    glTexCoord2f(0, 0)
                    glVertex3f(prev.x, prev.y, 0)
                    glTexCoord2f(p, 0)
                    glVertex3f(curr.x, curr.y, 0)
                    glTexCoord2f(p, 1)
                    glVertex3f(curr.x, curr.y, height)
                    glTexCoord2f(0, 1)
                    glVertex3f(prev.x, prev.y, height)
            glEnd()
            
            glBindTexture(GL_TEXTURE_2D, 0)
            
            
            glEndList()            

    def get_ear(self, coord: list[Vec2]):
        size = len(coord)

        if size < 3:
            return []

        if size == 3:
            triangle = [coord[0], coord[1], coord[2]]
            del coord[:]
            return triangle

        for i in range(size):
            tritest = False

            p1 = coord[(i - 1) % size]
            p2 = coord[i % size]
            p3 = coord[(i + 1) % size]

            if self.is_convex(p1, p2, p3):
                for x in coord:
                    if not (x in (p1, p2, p3)) and self.is_in_triangle(p1, p2, p3, x):
                        tritest = True

                if tritest == False:
                    del coord[i % size]
                    return [p1, p2, p3]
        return []

    def is_clockwise(self, coord: list[Vec2]):
        sum = (coord[0].x - coord[len(coord) - 1].x) * (coord[0].y + coord[len(coord) - 1].y)

        for i in range(len(coord) - 1):
            sum += (coord[i + 1].x - coord[i].x) * (coord[i + 1].y + coord[i].y)

        return sum > 0

    def is_convex(self, a: Vec2, b: Vec2, c: Vec2):
        crossp = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

        if crossp >= 0:
            return True

        return False

    def is_in_triangle(self, a: Vec2, b: Vec2, c: Vec2, p: Vec2):
        return (c.x - p.x) * (a.y - p.y) - (a.x - p.x) * (c.y - p.y) >= 0 and \
                (a.x - p.x) * (b.y - p.y) - (b.x - p.x) * (a.y - p.y) >= 0 and \
                (b.x - p.x) * (c.y - p.y) - (c.x - p.x) * (b.y - p.y) >= 0