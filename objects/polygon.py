from OpenGL.GL import *
from OpenGL.GLUT import *

from structures.vector import Vec2

class Polygon:
    def __init__(self, name: str, coords: list[Vec2]):
        self.name = name
        self.coords = coords
        
        self.center = Vec2(0, 0)
        self.width = 0
        
        self.name_size = Vec2(0, 0)
        
        self.triangles: list[Vec2] = []
        
        self.load()
    
    def draw(self):
        glBegin(GL_TRIANGLES)
        
        for point in self.triangles:
            glVertex2f(point.x, point.y)
            
        glEnd()
    
    def load(self):
        min = Vec2.min(*self.coords)
        max = Vec2.max(*self.coords)
        
        self.center = (min + max) / 2
        self.width = max.x - min.x
        
        self.name_size.x = sum(glutBitmapWidth(GLUT_BITMAP_9_BY_15, ord(c)) for c in self.name)
        self.name_size.y = glutBitmapHeight(GLUT_BITMAP_9_BY_15)
        
        if self.is_clockwise(self.coords):
            coords = self.coords[::-1]
        else:
            coords = self.coords[:]

        while len(coords) >= 3:
            a = self.get_ear(coords)
            if a == []:
                break

            self.triangles.extend(a)

    def is_clockwise(self, coord: list[Vec2]):
        sum = (coord[0].x - coord[len(coord) - 1].x) * (coord[0].y + coord[len(coord) - 1].y)

        for i in range(len(coord) - 1):
            sum += (coord[i + 1].x - coord[i].x) * (coord[i + 1].y + coord[i].y)

        return sum > 0

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

    def is_convex(self, a: Vec2, b: Vec2, c: Vec2):
        crossp = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

        if crossp >= 0:
            return True

        return False

    def is_in_triangle(self, a: Vec2, b: Vec2, c: Vec2, p: Vec2):
        return (c.x - p.x) * (a.y - p.y) - (a.x - p.x) * (c.y - p.y) >= 0 and \
                (a.x - p.x) * (b.y - p.y) - (b.x - p.x) * (a.y - p.y) >= 0 and \
                (b.x - p.x) * (c.y - p.y) - (c.x - p.x) * (b.y - p.y) >= 0