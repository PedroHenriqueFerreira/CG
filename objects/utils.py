from glm import vec2, radians
from math import sin, cos, asin, sqrt

class Utils:
    @staticmethod
    def haversine(a: vec2, b: vec2):
        
        a = radians(a)
        b = radians(b)

        delta = b - a

        c = 2 * asin(sqrt(sin(delta.x / 2) ** 2 + cos(a.x) * cos(b.x) * sin(delta.y / 2) ** 2))
        r = 6371.0088

        return r * c
