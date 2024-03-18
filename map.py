import json

from vector import Vector2

class Polygon:
    def __init__(self, coords: list[Vector2], type: str):
        self.coords = coords
        self.type = type

    def __repr__(self):
        return f'Polygon({self.coords})'

class Line:
    def __init__(self, coords: list[Vector2]):
        self.coords = coords

    def __repr__(self):
        return f'Line({self.coords})'

class Point:
    def __init__(self, coord: Vector2):
        self.coord = coord

    def __repr__(self):
        return f'Point({self.coord})'

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
            properties = feature['properties']

            if type == 'Polygon':
                coords_ = []
                
                for coord in coords[0]:
                    vector2 = Vector2(coord[0], coord[1])
                    
                    coords_.append(vector2)
                    self.updateMinMax(vector2)
                
                type_ = None
                
                for item in ['building', 'shop', 'amenity', 'tourism', 'man_made', 'club', 'office', 'natural']:
                    if type_ == 'yes':
                        type_ = None
                    
                    if type_ is None:
                        type_ = properties.get(item, None)
                    
                if type_ is None:
                    type_ = 'unknown'
                    
                self.polygons.append(Polygon(coords_, type_))
                
            elif type == 'LineString':
                coords_ = []
                
                for coord in coords:
                    vector2 = Vector2(coord[0], coord[1])
                    
                    coords_.append(vector2)
                    self.updateMinMax(vector2)
                
                self.lines.append(Line(coords_))
                
            else:
                vector2 = Vector2(coords[0], coords[1])
                
                self.points.append(Point(vector2))
                
if __name__ == '__main__':
    location = Map('russas.geojson')
