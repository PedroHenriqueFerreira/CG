from typing import Union

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
    
    def __sub__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x * other.x, self.y * other.y)
    
    def __truediv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x // other.x, self.y // other.y)
    
    def __pow__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vector2(other, other)
        
        return Vector2(self.x ** other.x, self.y ** other.y)
    
    def normalize(self):
        return self / (self.x ** 2 + self.y ** 2) ** 0.5