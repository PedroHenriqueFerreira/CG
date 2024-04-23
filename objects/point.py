from OpenGL.GL import *

from math import cos, sin, radians

from settings import POINT_SEGMENTS, POINT_WIDTH
from structures.vector import Vec2

triangles: list[Vec2] = []

def load():
    triangles.append(Vec2(0, 0))
    
    step = 360 / POINT_SEGMENTS
    
    for i in range(POINT_SEGMENTS + 1):
        x = cos(radians(i * step))
        y = sin(radians(i * step))
        
        triangles.append(0.5 * Vec2(x, y))

load()

class Point:
    def __init__(self, name: str, coord: Vec2):
        self.name = name
        self.coord = coord
    
        self.triangles = triangles
    
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.coord.x, self.coord.y, 0)
        glScalef(POINT_WIDTH, POINT_WIDTH, 1)
        
        glBegin(GL_TRIANGLE_FAN)
        
        for point in self.triangles:
            glVertex2f(point.x, point.y)
            
        glEnd()
        
        glPopMatrix()