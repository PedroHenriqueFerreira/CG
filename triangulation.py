import math
import sys

from vector import Vector2

EPSILON = math.sqrt(sys.float_info.epsilon)

def earclip(polygon: list[Vector2]):
    ear_vertex = []
    triangles: list[Vector2] = []

    if isCw(polygon):
        polygon.reverse()

    count_vert = len(polygon)
    
    for i in range(count_vert):
        prev_index = i - 1
        prev_vertex = polygon[prev_index]
        
        vertex = polygon[i]
        
        next_index = (i + 1) % count_vert
        next_vertex = polygon[next_index]

        if is_ear(prev_vertex, vertex, next_vertex, polygon):
            ear_vertex.append(vertex)

    while ear_vertex and count_vert >= 3:
        ear = ear_vertex.pop(0)
        
        i = polygon.index(ear)
        
        prev_index = i - 1
        prev_vertex = polygon[prev_index]
        
        next_index = (i + 1) % count_vert
        next_vertex = polygon[next_index]

        polygon.remove(ear)
        
        count_vert -= 1
        
        triangles.extend([prev_vertex, ear, next_vertex])
        
        if count_vert > 3:
            prev_prev_vertex = polygon[prev_index - 1]
            next_next_index = (i + 1) % count_vert
            next_next_vertex = polygon[next_next_index]

            groups = [
                (prev_prev_vertex, prev_vertex, next_vertex, polygon),
                (prev_vertex, next_vertex, next_next_vertex, polygon),
            ]
            
            for group in groups:
                p = group[1]
                
                if is_ear(*group):
                    if p not in ear_vertex:
                        ear_vertex.append(p)
                        
                elif p in ear_vertex:
                    ear_vertex.remove(p)
                    
    return triangles

def isCw(polygon: list[Vector2]):
    s = 0
    
    for i in range(len(polygon)):
        point = polygon[i]
        next_point = polygon[(i + 1) % len(polygon)]
        
        s += (next_point.x - point.x) * (next_point.y + point.y)
        
    return s > 0

def is_convex(prev, vertex, next):        
    return triangle_sum(prev.x, prev.y, vertex.x, vertex.y, next.x, next.y) < 0

def is_ear(p1, p2, p3, polygon):
    ear = no_int_vert(p1, p2, p3, polygon) and is_convex(p1, p2, p3) and triangle_area(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y) > 0
    return ear

def no_int_vert(p1, p2, p3, polygon):
    for pn in polygon:
        if pn in (p1, p2, p3):
            continue
        
        elif is_int_vert(pn, p1, p2, p3):
            return False
        
    return True

def is_int_vert(p, a, b, c):
    area = triangle_area(a.x, a.y, b.x, b.y, c.x, c.y)
    area1 = triangle_area(p.x, p.y, b.x, b.y, c.x, c.y)
    area2 = triangle_area(p.x, p.y, a.x, a.y, c.x, c.y)
    area3 = triangle_area(p.x, p.y, a.x, a.y, b.x, b.y)
    areadiff = abs(area - sum([area1, area2, area3])) < EPSILON
    
    return areadiff

def triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def triangle_sum(x1, y1, x2, y2, x3, y3):
    return x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)
