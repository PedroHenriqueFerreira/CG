from typing import Union
from math import sin, cos, radians

from structures.vector import Vec2

class Mat2:
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __repr__(self):
        return f'Mat2({[[self.a, self.b], [self.c, self.d]]})'

    def __add__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return Mat2(
            self.a + other.a,
            self.b + other.b,
            self.c + other.c,
            self.d + other.d
        )
    
    def __radd__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return other + self
    
    def __sub__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return Mat2(
            self.a - other.a, 
            self.b - other.b, 
            self.c - other.c, 
            self.d - other.d
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
                self.a * other.x + self.b * other.y, 
                self.c * other.x + self.d * other.y
            )
            
        return Mat2(
            self.a * other.a + self.b * other.c, 
            self.a * other.b + self.b * other.d, 
            self.c * other.a + self.d * other.c, 
            self.c * other.b + self.d * other.d
        )
        
    def __rmul__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return other * self        

    def __truediv__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return Mat2(
            self.a / other.a, 
            self.b / other.b, 
            self.c / other.c, 
            self.d / other.d
        )
        
    def __rtruediv__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return other / self
    
    def __floordiv__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return Mat2(
            self.a // other.a, 
            self.b // other.b, 
            self.c // other.c, 
            self.d // other.d
        )
        
    def __rfloordiv__(self, other: Union[float, 'Mat2']):
        if isinstance(other, float | int):
            other = Mat2(other, other, other, other)
            
        return other // self 

    @staticmethod
    def rotation(angle: float):
        sin_x = sin(radians(angle))
        cos_x = cos(radians(angle))
        
        return Mat2(cos_x, -sin_x, sin_x, cos_x)