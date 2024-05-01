from OpenGL.GL import *

from math import cos, sin, radians

from settings import LINE_STRING_WIDTH, POINT_SEGMENTS
from structures.vector import Vec2

def circle():
    triangles: list[Vec2] = [Vec2(0, 0)]
    
    step = 360 / POINT_SEGMENTS
    
    for i in range(POINT_SEGMENTS + 1):
        x = cos(radians(i * step))
        y = sin(radians(i * step))
        
        triangles.append(0.5 * Vec2(x, y))

    return triangles

triangles = circle()

class LineString:
    def __init__(self, name: str, coords: list[Vec2]):
        self.name = name
        self.coords = coords
        
        self.quads: list[Vec2] = []
        
        self.load()
    
    def draw(self):
        glBegin(GL_QUAD_STRIP)
        
        for point in self.quads:
            glVertex2f(point.x, point.y)
            
        glEnd()
        
        for coord in [self.coords[0], self.coords[-1]]:
            glPushMatrix()
            glTranslatef(coord.x, coord.y, 0)
            glScalef(LINE_STRING_WIDTH, LINE_STRING_WIDTH, 1)
            
            glBegin(GL_TRIANGLE_FAN)
            
            for point in triangles:
                glVertex2f(point.x, point.y)
                
            glEnd()
            
            glPopMatrix()

    
    def load(self):
        w = LINE_STRING_WIDTH / 2

        for prev, curr, next in zip([None] + self.coords[:-1], self.coords, self.coords[1:] + [None]):
            t0 = Vec2(0, 0) if prev is None else (curr - prev).normalize()
            t1 = Vec2(0, 0) if next is None else (next - curr).normalize()
            
            n0 = Vec2(-t0.y, t0.x)
            n1 = Vec2(-t1.y, t1.x)
            
            if prev is None:
                self.quads.extend([
                    curr + n1 * w,
                    curr - n1 * w,
                ])
                 
            elif next is None:
                self.quads.extend([
                    curr + n0 * w,
                    curr - n0 * w,
                ])
            else: 
                m = (n0 + n1).normalize()
                    
                dy = w / Vec2.dot(m, n1)
                
                self.quads.extend([
                    curr + m * dy,
                    curr - m * dy,
                ])