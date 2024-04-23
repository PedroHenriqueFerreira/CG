from OpenGL.GL import *

from settings import LINE_STRING_WIDTH
from structures.vector import Vec2

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