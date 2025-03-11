from OpenGL.GL import *

from structures.matrix import Mat2
from structures.vector import Vec2

from settings import CIRCLE_SEGMENTS

class Circle:
    def __init__(self, pos: Vec2, size: float, height: float, texture_size: float):
        self.pos = pos
        self.size = size
        self.height = height
        self.texture_size = texture_size
        
        self.positions: list[Vec2] = []
        
    def load(self):
        if len(self.positions) > 0:
            return
        
        step = 360 / CIRCLE_SEGMENTS
        
        self.positions.append(Vec2(0, 0))
        
        for i in range(CIRCLE_SEGMENTS + 1):
            self.positions.append(Mat2.rotation(i * step) * Vec2(0.5, 0))
        
        for i in range(len(self.positions)):
            self.positions[i] = self.positions[i] * self.size + self.pos
            
    def draw(self):
        self.load()
        
        glBegin(GL_TRIANGLE_FAN)
        
        for pos in self.positions:
            glNormal3f(0, 0, 1)
            glTexCoord2f(pos.x / self.texture_size, pos.y / self.texture_size)
            glVertex3f(pos.x, pos.y, self.height)
        
        glEnd()
        