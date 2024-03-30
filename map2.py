from json import loads
from vec import Vec2

from settings import LINE_WIDTH

class Point:
    def __init__(self, coord: Vec2):
        self.coord = coord
    
class LineString:
    def __init__(self, coords: list[Vec2]):
        self.coords = self.transform(coords)
    
    def transform(self, coords: list[Vec2]):
        width = LINE_WIDTH / 2
        
        triangles: list[list[Vec2]] = []

        for curr, next in zip(coords[:-1], coords[1:]):
            delta = (next - curr).normalize()

            normal = Vec2(-delta.y, delta.x) * width

            triangles.append([
                next + normal,
                curr + normal,
                curr - normal,
            ])
            
            triangles.append([
                curr - normal,
                next - normal,
                next + normal,
            ])          

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

        self.min = Vec2(float('inf'), float('inf'))
        self.max = Vec2(float('-inf'), float('-inf'))
    
        self.load()
    
    def load(self):
        with open(self.filepath, 'r') as f:
            data = loads(f.read())
        
        for feature in data['features']:
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
                
                case 'Polygon':
                    coords_ = [[Vec2(*point) for point in coord] for coord in coords]
                    self.polygons.append(Polygon(coords_))
                    
                    for coord_ in coords_:
                        self.min = Vec2.min(self.min, *coord_)
                        self.max = Vec2.max(self.max, *coord_)
            
if __name__ == '__main__':
    location = Map('russas.geojson')
    
          