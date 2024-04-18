from typing import Union
from math import radians, sin, cos, asin, sqrt

class Mat2:
    def __init__(self, a: float, b: float, c: float, d: float):
        self.data = [[a, b], [c, d]]

    def __repr__(self):
        return f'Mat2({self.data})'

    def __add__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return Mat2(
            self.data[0][0] + other.data[0][0], 
            self.data[0][1] + other.data[0][1], 
            self.data[1][0] + other.data[1][0], 
            self.data[1][1] + other.data[1][1]
        )
    
    def __radd__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return other + self
    
    def __sub__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return Mat2(
            self.data[0][0] - other.data[0][0], 
            self.data[0][1] - other.data[0][1], 
            self.data[1][0] - other.data[1][0], 
            self.data[1][1] - other.data[1][1]
        )
        
    def __rsub__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return other - self
    
    def __mul__(self, other: Union[float, 'Vec2', 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        if isinstance(other, Vec2):
            return Vec2(
                self.data[0][0] * other.x + self.data[0][1] * other.y, 
                self.data[1][0] * other.x + self.data[1][1] * other.y
            )
            
        return Mat2(
            self.data[0][0] * other.data[0][0] + self.data[0][1] * other.data[1][0], 
            self.data[0][0] * other.data[0][1] + self.data[0][1] * other.data[1][1], 
            self.data[1][0] * other.data[0][0] + self.data[1][1] * other.data[1][0], 
            self.data[1][0] * other.data[0][1] + self.data[1][1] * other.data[1][1]
        )
        
    def __rmul__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return other * self        

    @staticmethod
    def rotation_z(angle: float):
        return Mat2(cos(angle), -sin(angle), sin(angle), cos(angle))

class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vec2({self.x}, {self.y})'

    def __add__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other + self

    def __sub__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other - self

    def __mul__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)
            
        return Vec2(self.x * other.x, self.y * other.y)

    def __rmul__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other * self

    def __truediv__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x / other.x, self.y / other.y)

    def __rtruediv__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other / self

    def __floordiv__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x // other.x, self.y // other.y)

    def __rfloordiv__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other // self

    def __pow__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x ** other.x, self.y ** other.y)

    def __rpow__(self, other: Union[float, 'Vec2']):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other ** self

    def __eq__(self, other: 'Vec2'):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: 'Vec2'):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y))

    def radians(self):
        return Vec2(radians(self.x), radians(self.y))

    def normalize(self) -> 'Vec2':
        return self / (self.x ** 2 + self.y ** 2) ** 0.5

    def nearest(self, vectors: list['Vec2']):
        return min(vectors, key=lambda v: Vec2.distance(self, v))

    @staticmethod
    def dot(a: 'Vec2', b: 'Vec2') -> float:
        return a.x * b.x + a.y * b.y

    @staticmethod
    def center(*vectors: 'Vec2'):
        x = sum(v.x for v in vectors) / len(vectors)
        y = sum(v.y for v in vectors) / len(vectors)
        
        return Vec2(x, y)

    @staticmethod
    def min(*vectors: 'Vec2'):
        return Vec2(min(v.x for v in vectors), min(v.y for v in vectors))

    @staticmethod
    def max(*vectors: 'Vec2'):
        return Vec2(max(v.x for v in vectors), max(v.y for v in vectors))

    @staticmethod
    def distance(a: 'Vec2', b: 'Vec2') -> float:
        return ((b.x - a.x) ** 2 + (b.y - a.y) ** 2) ** 0.5

    @staticmethod
    def haversine(start: 'Vec2', goal: 'Vec2'):
        start = start.radians()
        goal = goal.radians()

        delta = goal - start

        a = sin(delta.x / 2) ** 2 + cos(start.x) * cos(goal.x) * sin(delta.y / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371.0088

        return r * c
