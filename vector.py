from typing import Union
from math import radians

ScalarType = Union[int, float]
OtherType = Union[ScalarType, 'Vector2']

class Vector2:
    def __init__(self, x: ScalarType, y: ScalarType):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'Vector2({self.x}, {self.y})'
        
    def __add__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __radd__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return other + self
    
    def __sub__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __rsub__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return other - self
    
    def __mul__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x * other.x, self.y * other.y)
    
    def __rmul__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return other * self
    
    def __truediv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x / other.x, self.y / other.y)
    
    def __rtruediv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return other / self
    
    def __floordiv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x // other.x, self.y // other.y)
    
    def __rfloordiv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return other // self
    
    def __pow__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x ** other.x, self.y ** other.y)
    
    def __rpow__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return other ** self
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other: 'Vector2'):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other: 'Vector2'):
        return not self == other
    
    def radians(self):
        return Vector2(radians(self.x), radians(self.y))
    
    def module(self) -> float:
        return (Vector2.dot(self, self)) ** 0.5
    
    def normalize(self):
        return self / self.module()

    @staticmethod
    def distance(a: 'Vector2', b: 'Vector2'):
        return (b - a).module()

    @staticmethod
    def dot(a: 'Vector2', b: 'Vector2'):
        return a.x * b.x + a.y * b.y

    @staticmethod
    def cross(a: 'Vector2', b: 'Vector2'):
        return a.x * b.y - a.y * b.x
    
    def closest(self, vectors: list['Vector2']):
        return min(vectors, key=lambda v: Vector2.distance(self, v))