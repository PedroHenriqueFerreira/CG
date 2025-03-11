from structures.vector import Vec2

class Triangle:
    def __init__(self, p1: Vec2, p2: Vec2, p3: Vec2):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        
    def is_convex(self):
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3

        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x) >= 0
    
    def contains(self, p: Vec2):
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3
        
        if p in (p1, p2, p3):
            return False
        
        return (
            (p3.x - p.x) * (p1.y - p.y) - (p1.x - p.x) * (p3.y - p.y) >= 0 and
            (p1.x - p.x) * (p2.y - p.y) - (p2.x - p.x) * (p1.y - p.y) >= 0 and
            (p2.x - p.x) * (p3.y - p.y) - (p3.x - p.x) * (p2.y - p.y) >= 0
        )