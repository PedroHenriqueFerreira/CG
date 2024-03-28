from typing import Union
from math import radians, sin, cos, asin, sqrt

ScalarType = Union[int, float]
OtherType = Union[ScalarType, 'Vec2']


class Vec2:
    def __init__(self, x: ScalarType, y: ScalarType):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vec2({self.x}, {self.y})'

    def __add__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x + other.x, self.y + other.y)

    def __radd__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other + self

    def __sub__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other - self

    def __mul__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x * other.x, self.y * other.y)

    def __rmul__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other * self

    def __truediv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x / other.x, self.y / other.y)

    def __rtruediv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other / self

    def __floordiv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x // other.x, self.y // other.y)

    def __rfloordiv__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other // self

    def __pow__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(self.x ** other.x, self.y ** other.y)

    def __rpow__(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return other ** self

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: 'Vec2'):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: 'Vec2'):
        return not self == other

    def min(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(min(self.x, other.x), min(self.y, other.y))

    def max(self, other: OtherType):
        if isinstance(other, float | int):
            other = Vec2(other, other)

        return Vec2(max(self.x, other.x), max(self.y, other.y))

    def radians(self):
        return Vec2(radians(self.x), radians(self.y))

    def normalize(self):
        return self / (self.x ** 2 + self.y ** 2) ** 0.5

    def nearest(self, vectors: list['Vec2']):
        return min(vectors, key=lambda v: Vec2.distance(self, v))

    @staticmethod
    def distance(a: 'Vec2', b: 'Vec2') -> ScalarType:
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
