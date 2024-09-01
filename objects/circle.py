from OpenGL.GL import *

from structures.matrix import Mat2
from structures.vector import Vec2

from settings import CIRCLE_SEGMENTS

circle = []

class Circle:
    def __init__(self, pos: Vec2, size: float):
        self.pos = pos
        self.size = size
        
        self.loaded = False
        
    def load(self):
        if len(circle) == 0:
            step = 360 / CIRCLE_SEGMENTS
            vec = Vec2(0.5, 0)
            
            circle.append(Vec2(0, 0))
            for i in range(CIRCLE_SEGMENTS + 1):
                circle.append(Mat2.rotation(i * step) * vec)
                
        self.loaded = True
            
    def draw(self):
        if not self.loaded:
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