from OpenGL.GL import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

from objects.circle import Circle

from objects.color import Color

from structures.vector import Vec2


class LineString:
    def __init__(self, map: 'Map', coords: list[Vec2], color: Color, size: float):
        self.map = map
        self.coords = coords
        self.size = size
        self.color = color

        self.circles: list[Circle] = []
        self.quads: list[Vec2] = []

        self.loaded = False
        self.gl_list = 0

    def load(self):
        self.size = self.map.km_to_world(self.size)

        self.circles.append(Circle(self.coords[0], self.size))
        self.circles.append(Circle(self.coords[-1], self.size))

        size = self.size / 2

        for prev, curr, next in zip([None] + self.coords[:-1], self.coords, self.coords[1:] + [None]):
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

        self.loaded = True

    def draw(self, texture = None):
        if not self.loaded:
            self.load()

        if self.gl_list > 0:
            glCallList(self.gl_list)
        else:
            self.gl_list = glGenLists(1)
            
            glNewList(self.gl_list, GL_COMPILE)

            glColor3f(self.color.r, self.color.g, self.color.b)

            if texture:
                glBindTexture(GL_TEXTURE_2D, texture.id)

            glBegin(GL_QUAD_STRIP)
            
            glNormal3f(0, 0, 1)
            
            for pos in self.quads:
                glVertex3f(pos.x, pos.y, 1e-5)
            
            glEnd()
            
            if texture:
                glBindTexture(GL_TEXTURE_2D, 0)
            
            for circle in self.circles:
                circle.draw()

            glEndList()
            
    def free(self):
        glDeleteLists([self.gl_list])