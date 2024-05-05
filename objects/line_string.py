from OpenGL.GL import *
from math import cos, sin, radians

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

from structures.vector import Vec2

from settings import LINE_STRING_SIZE, LINE_STRING_SEGMENTS

class LineString:
    def __init__(self, map: 'Map', coords: list[Vec2]):
        self.map = map
        self.coords = coords
        
        self.circle: list[Vec2] = []
        self.quads: list[Vec2] = []

        self.loaded = False

    def load(self):
        width = self.map.transform_km(LINE_STRING_SIZE) / 2

        for prev, curr, next in zip([None] + self.coords[:-1], self.coords, self.coords[1:] + [None]):
            t0 = Vec2(0, 0) if prev is None else (curr - prev).normalize()
            t1 = Vec2(0, 0) if next is None else (next - curr).normalize()

            n0 = Vec2(-t0.y, t0.x)
            n1 = Vec2(-t1.y, t1.x)

            if prev is None:
                self.quads.extend([curr + n1 * width, curr - n1 * width])

            elif next is None:
                self.quads.extend([curr + n0 * width, curr - n0 * width])

            else:
                m = (n0 + n1).normalize()

                dy = width / Vec2.dot(m, n1)

                self.quads.extend([curr + m * dy, curr - m * dy])

        step = 360 / LINE_STRING_SEGMENTS
        
        self.circle.append(Vec2(0, 0))
        
        for i in range(LINE_STRING_SEGMENTS + 1):
            x = cos(radians(i * step))
            y = sin(radians(i * step))
            
            self.circle.append(Vec2(x, y) * width)

        self.loaded = True

    def draw(self):
        if not self.loaded:
            self.load()

        glBegin(GL_QUAD_STRIP)
        for point in self.quads:
            glVertex2f(point.x, point.y)
        glEnd()

        for pos in [self.coords[0], self.coords[-1]]:
            glPushMatrix()
            
            glTranslatef(pos.x, pos.y, 0)
            glBegin(GL_TRIANGLE_FAN)
            for point in self.circle:
                glVertex2f(pos.x, pos.y)
            glEnd()
            
            glPopMatrix()