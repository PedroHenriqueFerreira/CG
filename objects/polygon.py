from OpenGL.GL import *
from OpenGL.GLUT import *

from objects.texture import Texture2D
from objects.color import Color
from structures.vector import Vec2

class Polygon:
    def __init__(
        self,
        coords: list[Vec2],
        height: float,
        color: Color,
        texture: Texture2D, 
        texture_size: float
    ):
        self.coords = coords
        self.height = height
        self.color = color
        self.texture = texture
        self.texture_size = texture_size
        
        self.triangles: list[Vec2] = []
        self.gl_list = 0
    
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

    def draw(self):    
        if self.gl_list > 0:
            return glCallList(self.gl_list)
        
        self.load()
        self.texture.load()
        
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
        glColor3f(self.color.r, self.color.g, self.color.b)
        
        glBegin(GL_TRIANGLES)
        
        glNormal3f(0, 0, 1)
        
        for point in self.triangles:
            glTexCoord2f(point.x / self.texture_size, point.y / self.texture_size)
            glVertex3f(point.x, point.y, self.height)
        
        glEnd()
        
        glBegin(GL_QUADS)
        
        for prev, curr in zip(self.coords[:-1], self.coords[1:]):
            vector = curr - prev
            
            normal = vector.normalize()
            length = vector.length()
            
            glNormal3f(-normal.y, normal.x, 0)
            
            glTexCoord2f(0, 0)
            glVertex3f(prev.x, prev.y, 0)
            glTexCoord2f(length / self.texture_size, 0)
            glVertex3f(curr.x, curr.y, 0)
            glTexCoord2f(length / self.texture_size, self.height / self.texture_size)
            glVertex3f(curr.x, curr.y, self.height)
            glTexCoord2f(0, self.height / self.texture_size)
            glVertex3f(prev.x, prev.y, self.height)
        
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