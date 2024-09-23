from OpenGL.GL import *

from objects.circle import Circle
from objects.texture import Texture2D

from structures.vector import Vec2, Vec3

class LineString:
    def __init__(
        self, 
        coords: list[Vec2], 
        height: float,
        color: Vec3, 
        size: float,
        texture: Texture2D,
        texture_size: float
    ):
        self.coords = coords
        self.height = height
        self.color = color
        self.size = size
        self.texture = texture
        self.texture_size = texture_size

        self.circles: list[Circle] = []
        self.quads: list[Vec2] = []
        self.gl_list = 0

    def load(self):
        if len(self.quads) > 0:
            return

        self.circles.append(Circle(self.coords[0], self.size))
        self.circles.append(Circle(self.coords[-1], self.size))

        size = self.size / 2
        
        prev_coords = [None] + self.coords[:-1]
        next_coords = self.coords[1:] + [None]
        
        for prev, curr, next in zip(prev_coords, self.coords, next_coords):
            t0 = Vec2(0, 0) if prev is None else (curr - prev).normalize()
            t1 = Vec2(0, 0) if next is None else (next - curr).normalize()

            n0 = Vec2(-t0.y, t0.x)
            n1 = Vec2(-t1.y, t1.x)

            if prev is None:
                self.quads.extend([curr + n1 * size, curr - n1 * size])

            elif next is None:
                self.quads.extend([curr + n0 * size, curr - n0 * size])

            else:
                m = (n0 + n1).normalize()

                dy = size / Vec2.dot(m, n1)

                self.quads.extend([curr + m * dy, curr - m * dy])

    def draw(self):
        if self.gl_list > 0:
            return glCallList(self.gl_list)
        
        self.load()
        self.texture.load()

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)

        glColor3f(self.color.x, self.color.y, self.color.z)

        glBegin(GL_QUAD_STRIP)
        
        glNormal3f(0, 0, 1)
        
        for pos in self.quads:
            glTexCoord2f(pos.x / self.texture_size, pos.y / self.texture_size)
            glVertex3f(pos.x, pos.y, self.height)
        
        glEnd()
        
        glPushMatrix()
        
        glTranslatef(0, 0, -self.height)
        
        for circle in self.circles:
            circle.draw()
            
        glPopMatrix()

        glBindTexture(GL_TEXTURE_2D, 0)
        glEndList()
