from OpenGL.GL import *

from structures.vector import Vec2
from structures.matrix import Mat2

from objects.texture import Texture

from settings import CAR_TEXTURE, CAR_FORWARD_SPEED, CAR_BACKWARD_SPEED, CAR_ROTATION_SPEED, CAR_WIDTH

class Car:
    def __init__(self):
        self.texture = Texture(CAR_TEXTURE)
        
        self.pos = Vec2(0, 0)      
        
        self.i = Vec2(1, 0)
        self.j = Vec2(0, 1)

    def move(self, distance: float):
        self.pos += self.j * distance

    def move_forward(self):
        self.move(CAR_FORWARD_SPEED)
        
    def move_backward(self):
        self.move(-CAR_BACKWARD_SPEED)
        
    def rotate(self, angle: float):
        self.i = Mat2.rotation(angle) * self.i
        self.j = Mat2.rotation(angle) * self.j
        
    def rotate_left(self):
        self.rotate(CAR_ROTATION_SPEED * 360)
        
    def rotate_right(self):
        self.rotate(-CAR_ROTATION_SPEED * 360)
        
    def matrix(self):
        return [
            [self.i.x, self.i.y, 0, 0], 
            [self.j.x, self.j.y, 0, 0], 
            [0, 0, 1, 0], 
            [self.pos.x, self.pos.y, 0, 1]
        ]
        
    def draw(self):    
        w = CAR_WIDTH / 2
        
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        glPushMatrix()
        glMultMatrixf(self.matrix())
        glBegin(GL_QUADS)
        
        glTexCoord2f(0, 0)
        glVertex2f(-w, -w)
        glTexCoord2f(1, 0)
        glVertex2f(+w, -w)
        glTexCoord2f(1, 1)
        glVertex2f(+w, +w)
        glTexCoord2f(0, 1)
        glVertex2f(-w, +w)
        
        glEnd()
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)
        
        
        