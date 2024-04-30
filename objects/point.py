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
    
    def draw(self, rotate: float, scale: float, texture: int):
        glBindTexture(GL_TEXTURE_2D, texture)
        glPushMatrix()
    
        glTranslatef(self.coord.x, self.coord.y, 0)
        glScalef(POINT_WIDTH, POINT_WIDTH, 1)
        
        glRotatef(rotate, 0, 0, 1)
        glScalef(scale, scale, 1)
        
        glBegin(GL_TRIANGLE_FAN)
        
        # for point in self.triangles:
        #     glVertex2f(point.x, point.y)
        
        glTexCoord2f(0, 0)
        glVertex2f(-0.5, -0.5)
        glTexCoord2f(1, 0)
        glVertex2f(0.5, -0.5)
        glTexCoord2f(1, 1)
        glVertex2f(0.5, 0.5)
        glTexCoord2f(0, 1)
        glVertex2f(-0.5, 0.5)
            
        glEnd()
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)