import json

from vector import Vector2

from triangulation import earclip

class Polygon:
    def __init__(self, coords: list[list[Vector2]], type: str | None):
        # self.coords: list[list[Vector2]] = coords
        self.type = type
        
        # print(coords[0])
        
        self.coords = coords
        
        # for coord in coords:
        #     triangle = earclip(coord[:])
        
        #     # print(triangles)
            
        #     # if len(triangles) == 0:
        #     #     self.coords.append(coord)
        #     # else:
            
        #     if len(triangle) == 0:
        #         self.coords.append(coord)
        #     else:
        #         self.triangles.append(triangle)

    def __repr__(self):
        return f'Polygon({self.coords, self.type})'

    def triangulate(self, coord: list[Vector2]):
        triangules: list[Vector2] = []
        
        # last = -1
        
        while len(coord) > 3:
            # if last == len(coord):
            #     print('Error')
            #     triangules.clear()
            #     break
            
            # last = len(coord)
            
            for i in range(len(coord)):
                if self.isEar(coord, i):
                    prev = (i - 1) % len(coord)
                    next = (i + 1) % len(coord)
                    
                    triangules.extend([coord[prev], coord[i], coord[next]])
                    
                    del coord[i]
                    break
                
        triangules.extend(coord)
        
        return triangules
        
    def isEar(self, coord: list[Vector2], i: int):
        prev = (i - 1) % len(coord)
        next = (i + 1) % len(coord)
        
        p_prev, p, p_next = coord[prev], coord[i], coord[next]
        
        if Vector2.cross(p_next - p, p_prev - p) >= 0:
            return False
        
        for j in range(len(coord)):
            if j not in (prev, i, next):
                if self.isPointInTriangle(coord[j], p_prev, p, p_next):
                    return False
            
        return True
        
    def isPointInTriangle(self, p: Vector2, p1: Vector2, p2: Vector2, p3: Vector2):
        def sign(pt1, pt2, pt3):
            return (pt1.x - pt3.x) * (pt2.y - pt3.y) - (pt2.x - pt3.x) * (pt1.y - pt3.y)
    
        d1 = sign(p, p1, p2)
        d2 = sign(p, p2, p3)
        d3 = sign(p, p3, p1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)
        
class Line:
    def __init__(self, coords: list[Vector2]):
        self.coords = coords

    def __repr__(self):
        return f'Line({self.coords})'

class Point:
    def __init__(self, coord: Vector2, type: str | None = None):
        self.coord = coord
        self.type = type

    def __repr__(self):
        return f'Point({self.coord, self.type})'

class Map:
    def __init__(self, file: str):
        self.file = file
        
        self.polygons: list[Polygon] = []
        self.lines: list[Line] = []
        self.points: list[Point] = []  
        
        self.min = Vector2(float('inf'), float('inf'))
        self.max = Vector2(float('-inf'), float('-inf'))
        
        self.load()
        
    def __repr__(self):
        return f'Map({self.file})'
        
    def updateMinMax(self, coord: Vector2):
        self.min.x = min(self.min.x, coord.x)
        self.max.x = max(self.max.x, coord.x)
        self.min.y = min(self.min.y, coord.y)
        self.max.y = max(self.max.y, coord.y)
    
    def uniquePolygonTypes(self):
        types = set()
        
        for polygon in self.polygons:
            types.add(polygon.type)
                
        return list(types)
    
    def load(self):
        with open(self.file, 'r') as f:
            data = json.loads(f.read())
            
        for feature in data['features']:
            type = feature['geometry']['type']
            coords = feature['geometry']['coordinates']
            
            properties = feature['properties'] # TODO: Use properties

            if type == 'Polygon':
                if properties.get('type') == 'boundary':
                    continue
                
                coords_ = []
                
                for coord in coords:
                    coord_ = []
                    
                    for x, y in coord:
                        point = Vector2(x, y)
                        
                        coord_.append(point)
                        self.updateMinMax(point)
                        
                    coords_.append(coord_)
                
                type_ = None
                
                if properties.get('natural', None) == 'water':
                    type_ = 'water'
                
                if properties.get('natural', None) == 'wood':
                    type_ = 'wood'
                
                self.polygons.append(Polygon(coords_, type_))
                
            elif type == 'LineString':
                if properties.get('highway') in ('track', 'footway', 'pedestrian', 'cycleway'):
                    continue
                
                coords_ = []
                
                for x, y in coords:
                    point = Vector2(x, y)
                    
                    coords_.append(point)
                    self.updateMinMax(point)
                    
                self.lines.append(Line(coords_))
                
            elif type == 'Point':
                point = Vector2(coords[0], coords[1])
                
                type_ = None
                
                if properties.get('natural', None) == 'tree':
                    type_ = 'tree'
                
                self.points.append(Point(point, type_))
                self.updateMinMax(point)
                            
if __name__ == '__main__':
    location = Map('russas.geojson')
