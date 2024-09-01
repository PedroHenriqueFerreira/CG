from random import random

class Color:
    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b
        
    @staticmethod
    def random():
        return Color(random(), random(), random())
    
    @staticmethod
    def hex(value: str):
        return Color(*[int(value.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4)])