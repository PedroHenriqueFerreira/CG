from OpenGL.GL import *

from structures.matrix import Mat2
from structures.vector import Vec2

from settings import CIRCLE_SEGMENTS

circle = []

class Circle:
    def __init__(self, pos: Vec2, size: float):
        self.pos = pos
        self.size = size
        
    def load(self):
        if len(circle) > 0:
            return
        
        step = 360 / CIRCLE_SEGMENTS
        
        circle.append(Vec2(0, 0))
        
        for i in range(CIRCLE_SEGMENTS + 1):
            circle.append(Mat2.rotation(i * step) * Vec2(0.5, 0))
            
    def draw(self):
        self.load()
        
        glPushMatrix()
        
        glTranslatef(self.pos.x, self.pos.y, 0)
        glScalef(self.size, self.size, 1)
        
        glBegin(GL_TRIANGLE_FAN)
        
        glNormal3f(0, 0, 1)
        for pos in circle:
            glVertex3f(pos.x, pos.y, 0)
        
        glEnd()
        
        glPopMatrix()