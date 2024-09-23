from typing import Union, Callable
from math import radians, sin, cos, asin, sqrt, acos, degrees

from numpy import array

class Vec:
    ''' Vector class '''
    
    def __init__(self, *values: float):
        self.values = values
        
        self.n = len(values)
        
    def __repr__(self):
        return f'Vec({", ".join(str(v) for v in self.values)})'

    def op(self, other: Union[int, float, 'Vec'], func: Callable[[float, float], float]):
        ''' Perform operation between two vectors '''
        
        if isinstance(other, int | float):
            return self.__class__(*[func(self.values[i], other) for i in range(self.n)])

        if self.n != other.n:
            raise ValueError('Vectors must have the same length')

        return self.__class__(*[func(self.values[i], other.values[i]) for i in range(self.n)])

    def rop(self, other: Union[int, float], func: Callable[[float, float], float]):
        ''' Perform operation between scalar and vector '''
        
        return self.__class__(*[func(other, self.values[i]) for i in range(self.n)])

    def __add__(self, other: Union[int, float, 'Vec']):
        return self.op(other, lambda a, b: a + b)

    def __radd__(self, other: Union[int, float]):
        return self.rop(other, lambda a, b: a + b)

    def __sub__(self, other: Union[int, float, 'Vec']):
        return self.op(other, lambda a, b: a - b)

    def __rsub__(self, other: Union[int, float]):
        return self.rop(other, lambda a, b: a - b)

    def __mul__(self, other: Union[int, float, 'Vec']):
        return self.op(other, lambda a, b: a * b)
    
    def __rmul__(self, other: Union[int, float]):
        return self.rop(other, lambda a, b: a * b)
    
    def __truediv__(self, other: Union[int, float, 'Vec']):
        return self.op(other, lambda a, b: a / b)
    
    def __rtruediv__(self, other: Union[int, float]):
        return self.rop(other, lambda a, b: a / b)
    
    def __floordiv__(self, other: Union[int, float, 'Vec']):
        return self.op(other, lambda a, b: a // b)
    
    def __rfloordiv__(self, other: Union[int, float]):
        return self.rop(other, lambda a, b: a // b)

    def __pow__(self, other: Union[int, float, 'Vec']):
        return self.op(other, lambda a, b: a ** b)
    
    def __rpow__(self, other: Union[int, float]):
        return self.rop(other, lambda a, b: a ** b)

    def __eq__(self, other: 'Vec'):
        return self.values == other.values
    
    def __ne__(self, other: 'Vec'):
        return not self == other

    def __hash__(self):
        return hash(self.values)

    def length(self) -> float:
        ''' Calculate vector length '''
        
        return sum(v ** 2 for v in self.values) ** 0.5
    
    def distance(self, other: 'Vec') -> float:
        ''' Calculate distance between two vectors '''
        
        if self.n != other.n:
            raise ValueError('Vectors must have the same length')
        
        return sum((self.values[i] - other.values[i]) ** 2 for i in range(self.n)) ** 0.5
    
    def dot(self, other: 'Vec') -> float:
        ''' Calculate dot product '''
        
        if self.n != other.n:
            raise ValueError('Vectors must have the same length')
        
        return sum(self.values[i] * other.values[i] for i in range(self.n))
    
    def radians(self):
        ''' Convert vector values to radians '''
        
        return self.__class__(*[radians(v) for v in self.values])

    def normalize(self):
        ''' Normalize vector '''
        
        if self.length() == 0:
            return self.__class__(*[0 for _ in self.values])
        
        return self / self.length()

    def nearest(self, *vectors: 'Vec'):
        ''' Find nearest vector '''
        
        return min(vectors, key=lambda v: self.distance(v))
    
    def __array__(self, dtype=None):
        return array(self.values, dtype=dtype)

    @staticmethod
    def min(*vectors: 'Vec'):
        ''' Find minimum vector '''
        
        cls = vectors[0].__class__
        
        return cls(*[min(values) for values in zip(*[vector.values for vector in vectors])])

    @staticmethod
    def max(*vectors: 'Vec'):
        ''' Find maximum vector '''
        
        cls = vectors[0].__class__
        
        return cls(*[max(values) for values in zip(*[vector.values for vector in vectors])])
        
class Vec2(Vec):
    ''' 2D vector class '''
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'Vec2({self.x}, {self.y})'
        
    def angle(self, other: 'Vec2'):
        ''' Calculate angle between two vectors '''
        
        self_norm = self.normalize()
        other_norm = other.normalize()
        
        cos = min(max(self_norm.dot(other_norm), -1), 1)
        
        degrees_angle = degrees(acos(cos))
        
        sign = 1 if (self.x * other.y - self.y * other.x) > 0 else -1
        
        return sign * degrees_angle

    def haversine(self, other: 'Vec2'):
        ''' Calculate haversine distance between two vectors '''
        
        self_radians = self.radians()
        other_radians = other.radians()

        delta = other_radians - self_radians

        a = sin(delta.x / 2) ** 2 + cos(self_radians.x) * cos(other_radians.x) * sin(delta.y / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371.0088

        return r * c

    def to_vec3(self, z: float):
        ''' Convert 2D vector to 3D vector '''
        
        return Vec3(self.x, self.y, z)

class Vec3(Vec):
    ''' 3D vector class '''
    
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)
        
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Vec3({self.x}, {self.y}, {self.z})'
    
    @staticmethod
    def from_hex(value: str):
        return Vec3(*[int(value.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4)])