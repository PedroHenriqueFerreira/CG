from math import cos, sin, radians
from structures.vector import Vec2

from settings import CIRCLE_SEGMENTS

def circle_coords():
    coords: list[Vec2] = [Vec2(0, 0)]
    
    step = 360 / CIRCLE_SEGMENTS
    
    for i in range(CIRCLE_SEGMENTS + 1):
        x = cos(radians(i * step))
        y = sin(radians(i * step))
        
        coords.append(0.5 * Vec2(x, y))

    return coords

circle = circle_coords()

