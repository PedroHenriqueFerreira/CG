from json import loads
from vec import Vec2

from settings import LINE_WIDTH

class Point:
    def __init__(self, coord: Vec2):
        self.coord = coord
    
class LineString:
    def __init__(self, coords: list[Vec2]):
        self.coords = coords
        
        self.triangles = self.transform(coords)
    
    def transform(self, coords: list[Vec2]):
        w = LINE_WIDTH / 2
        
        lines: list[list[Vec2]] = []

        for prev, curr, next in zip([None] + coords[:-1], coords, coords[1:] + [None]):
            t0 = Vec2(0, 0) if prev is None else (curr - prev).normalize()
            t1 = Vec2(0, 0) if next is None else (next - curr).normalize()
            
            n0 = Vec2(-t0.y, t0.x)
            n1 = Vec2(-t1.y, t1.x)
            
            if prev is None:
                lines.append([
                    curr + n1 * w, #- t1 * w,
                    curr - n1 * w, #- t1 * w,
                ])
                 
            elif next is None:
                lines.append([
                    curr + n0 * w, #+ t0 * w,
                    curr - n0 * w, #+ t0 * w,
                ])
            else: 
                m = (n0 + n1).normalize()
                    
                dy = w / Vec2.dot(m, n1)
                
                lines.append([
                    curr + m * dy,
                    curr - m * dy,
                ])

        triangles: list[list[Vec2]] = []
        
        for curr, next in zip(lines[:-1], lines[1:]):
            triangles.append([curr[0], curr[1],  next[0]])
            triangles.append([next[0], next[1], curr[1]])

        return triangles
    
class Polygon:
    def __init__(self, coords: list[list[Vec2]]):
        self.coords = coords

class Map:
    def __init__(self, filepath: str):
        self.filepath = filepath

        self.points: list[Point] = []
        self.line_strings: list[LineString] = []
        self.polygons: list[Polygon] = []
        
        self.graph: dict[Vec2, list[Vec2]] = {}

        self.min = Vec2(float('inf'), float('inf'))
        self.max = Vec2(float('-inf'), float('-inf'))
    
        self.load()
    
    def load(self):
        with open(self.filepath, 'r') as f:
            data = loads(f.read())
        
        for feature in data['features']:
            properties = feature['properties']
            
            type = feature['geometry']['type']
            coords = feature['geometry']['coordinates']
            
            match type:
                case 'Point':
                    coords_ = Vec2(*coords)
                    self.points.append(Point(coords_))
                    
                    self.min = Vec2.min(self.min, coords_)
                    self.max = Vec2.max(self.max, coords_)
                
                case 'LineString':
                    coords_ = [Vec2(*coord) for coord in coords]
                    
                    self.line_strings.append(LineString(coords_))
                    
                    self.min = Vec2.min(self.min, *coords_)
                    self.max = Vec2.max(self.max, *coords_)
                    
                    for prev, curr, next in zip([None] + coords_[:-1], coords_, coords_[1:] + [None]):
                        if curr not in self.graph:
                            self.graph[curr] = []
                            
                        if prev and prev not in self.graph[curr]:
                            self.graph[curr].append(prev)
                    
                        if next and next not in self.graph[curr]:
                            self.graph[curr].append(next)
                
                case 'Polygon':
                    coords_ = [[Vec2(*point) for point in coord] for coord in coords]
                    self.polygons.append(Polygon(coords_))
                    
                    for coord_ in coords_:
                        self.min = Vec2.min(self.min, *coord_)
                        self.max = Vec2.max(self.max, *coord_)
        
if __name__ == '__main__':
    location = Map('russas.geojson')