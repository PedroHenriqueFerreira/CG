import json

from vector import Vector2

class Polygon:
    def __init__(self, coords: list[Vector2]):
        self.coords = coords

    def __repr__(self):
        return f'Polygon({self.coords})'

class Line:
    def __init__(self, coords: list[Vector2]):
        self.coords = coords

    def __repr__(self):
        return f'Line({self.coords})'

class Map:
    def __init__(self, file: str):
        self.file = file
        
        self.polygons: list[Polygon] = []
        self.lines: list[Line] = []
          
        self.min = Vector2(float('inf'), float('inf'))
        self.max = Vector2(float('-inf'), float('-inf'))
        
        self.load()
        
    def __repr__(self):
        return f'Map({self.file})'
        
    def updateMinMax(self, x, y):
        self.min.x = min(self.min.x, x)
        self.max.x = max(self.max.x, x)
        self.min.y = min(self.min.y, y)
        self.max.y = max(self.max.y, y)
    
    def load(self):
        with open(self.file, 'r') as f:
            data = json.loads(f.read())
            
        for feature in data['features']:
            type = feature['geometry']['type']
            coords = feature['geometry']['coordinates']

            if type == 'Polygon':
                coords_ = []
                
                for coord in coords[0]:
                    coords_.append(Vector2(coord[0], coord[1]))
                    self.updateMinMax(coord[0], coord[1])
                    
                self.polygons.append(Polygon(coords_))
                
            elif type == 'LineString':
                coords_ = []
                
                for coord in coords:
                    coords_.append(Vector2(coord[0], coord[1]))
                    self.updateMinMax(coord[0], coord[1])
                
                self.lines.append(Line(coords_))
        
if __name__ == '__main__':
    location = Map('russas.geojson')
