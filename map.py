import math
import json

from vector import Vector2

class Polygon:
    def __init__(
        self, 
        name: str | None = None, 
        coords: list[list[Vector2]] | None = None, 
        type: str | None = None
    ):
        self.name = name
        self.coords = coords
        
        self.triangles = [self.triangulate(coord) for coord in coords]

        self.type = type

        self.min = self.min()
        self.max = self.max()
        self.centroid = self.centroid()

    def min(self):
        x = min([point.x for coord in self.coords for point in coord])
        y = min([point.y for coord in self.coords for point in coord])

        return Vector2(x, y)

    def max(self):
        x = max([point.x for coord in self.coords for point in coord])
        y = max([point.y for coord in self.coords for point in coord])

        return Vector2(x, y)

    def centroid(self):
        size = sum([len(coord) for coord in self.coords])
        
        x = sum([point.x for coord in self.coords for point in coord]) / size
        y = sum([point.y for coord in self.coords for point in coord]) / size

        return Vector2(x, y)

    def triangulate(self, polygon: list[Vector2]):
        triangles: list[Vector2] = []
        
        if self.isClockwise(polygon):
            polygon = polygon[::-1]
        else:
            polygon = polygon[:]
        
        while len(polygon) >= 3:
            a = self.getEar(polygon)
            if a == []:
                break
            
            triangles.extend(a)
        return triangles

    def isClockwise(self, polygon: list[Vector2]):
        # initialize sum with last element
        sum = (polygon[0].x - polygon[len(polygon) - 1].x) * (polygon[0].y + polygon[len(polygon) - 1].y)
        
        # iterate over all other elements (0 to n-1)
        for i in range(len(polygon) - 1):
            sum += (polygon[i + 1].x - polygon[i].x) * (polygon[i + 1].y + polygon[i].y)
        
        return sum > 0

    def getEar(self, polygon: list[Vector2]):
        size = len(polygon)
        
        if size < 3:
            return []
        
        if size == 3:
            tri = [polygon[0], polygon[1], polygon[2]]
            del polygon[:]
            return tri
        
        for i in range(size):
            tritest = False
            
            p1 = polygon[(i - 1) % size]
            p2 = polygon[i % size]
            p3 = polygon[(i + 1) % size]
            
            if self.isConvex(p1, p2, p3):
                for x in polygon:
                    if not (x in (p1, p2, p3)) and self.inTriangle(p1, p2, p3, x):
                        tritest = True
                        
                if tritest == False:
                    del polygon[i % size]
                    return [p1, p2, p3]
        return []

    def isConvex(self, a: Vector2, b: Vector2, c: Vector2):
        # only convex if traversing anti-clockwise!
        crossp = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
        
        if crossp >= 0:
            return True 
        
        return False 

    def inTriangle(self, a: Vector2, b: Vector2, c: Vector2, p: Vector2):
        L = [0, 0, 0]
        eps = 0.0000001
        # calculate barycentric coefficients for point p
        # eps is needed as error correction since for very small distances denom->0
        L[0] = ((b.y - c.y) * (p.x - c.x) + (c.x - b.x) * (p.y - c.y)) \
            /(((b.y - c.y) * (a.x - c.x) + (c.x - b.x) * (a.y - c.y)) + eps)
            
        L[1] = ((c.y - a.y) * (p.x - c.x) + (a.x - c.x) * (p.y - c.y)) \
            /(((b.y - c.y) * (a.x - c.x) + (c.x - b.x) * (a.y - c.y)) + eps)
            
        L[2] = 1 - L[0] - L[1]
        
        # check if p lies in triangle (a, b, c)
        for x in L:
            if x >= 1 or x <= 0:
                return False  
            
        return True  

class Line:
    def __init__(self, name: str | None, coords: list[Vector2] | None = None):
        self.name = name
        self.coords = coords
        
        self.quads = self.fourangulate(coords)

    def fourangulate(self, coords: list[Vector2]):
        width = 0.00005
        
        quads: list[list[Vector2]] = []
        
        for prev, curr in zip(coords[:-1], coords[1:]):
            prev_curr = curr - prev
            
            prev_curr_normal = Vector2(-prev_curr.y, prev_curr.x).normalize()
            
            p0 = prev + prev_curr_normal * (width / 2)
            p1 = prev - prev_curr_normal * (width / 2)
            p2 = curr - prev_curr_normal * (width / 2)
            p3 = curr + prev_curr_normal * (width / 2)
            
            quads.append([p0, p1, p2, p3])
            
        return quads
     
class Map:
    def __init__(self, file: str):
        self.file = file

        self.polygons: list[Polygon] = []
        self.lines: list[Line] = []
        
        self.relations: dict[Vector2, list[Vector2]] = {}

        self.min = Vector2(float('inf'), float('inf'))
        self.max = Vector2(float('-inf'), float('-inf'))

        self.load()

    def __repr__(self):
        return f'Map({self.file})'  

    def updateBorder(self, coord: Vector2):
        self.min.x = min(self.min.x, coord.x)
        self.max.x = max(self.max.x, coord.x)
        self.min.y = min(self.min.y, coord.y)
        self.max.y = max(self.max.y, coord.y)

    def load(self):
        with open(self.file, 'r') as f:
            data = json.loads(f.read())

        for feature in data['features']:
            type = feature['geometry']['type']
            coords: list[list[float]] = feature['geometry']['coordinates']

            properties = feature['properties']
            name_ = properties.get('name')

            if type == 'Polygon':
                if properties.get('type') == 'boundary':
                    continue
                
                if properties.get('leisure') == 'park':
                    continue

                coords_ = []

                for coord in coords:
                    coord_ = []

                    for x, y in coord[:-1]:
                        point = Vector2(x, y)

                        coord_.append(point)
                        self.updateBorder(point)

                    coords_.append(coord_)

                type_ = 'building'

                if properties.get('landuse') in (
                    'basin',
                    'salt_pond',
                ) or properties.get('leisure') in (
                    'swimming_pool',
                ) or properties.get('natural') in (
                    'reef',
                    'water',
                ):
                    type_ = 'water'

                if properties.get('landuse') in (
                    'allotments',
                    'flowerbed',
                    'forest',
                    'meadow',
                    'orchard',
                    'plant_nursery',
                    'vineyard',
                    'cemetery',
                    'grass',
                    'recreation_ground',
                    'village_green',
                ) or properties.get('leisure') in (
                    'garden',
                    'pitch',
                ) or properties.get('natural') in (
                    'grassland',
                    'heath',
                    'scrub',
                    'wood',
                    'wetland',
                ):
                    type_ = 'grass'

                if properties.get('natural') in (
                    'beach',
                    'sand'
                ):
                    type_ = 'sand'

                self.polygons.append(Polygon(name_, coords_, type_))

            elif type == 'LineString':
                if properties.get('highway') not in (
                    'motorway',
                    'trunk',
                    'primary',
                    'secondary',
                    'tertiary',
                    'unclassified',
                    'residential',
                    'motorway_link',
                    'trunk_link',
                    'primary_link',
                    'secondary_link',
                    'tertiary_link',
                    'living_street',
                    'service',
                    'pedestrian',
                    'raceway',
                    'road',
                ):
                    continue

                coords_: list[Vector2] = []

                for prev, curr, next in zip([None] + coords[:-1], coords, coords[1:] + [None]):
                    point = Vector2(*curr)

                    coords_.append(point)
                    self.updateBorder(point)
                    
                    if point not in self.relations:
                        self.relations[point] = []
                        
                    if prev is not None:
                        prev_point = Vector2(*prev)
                        
                        if prev_point not in self.relations:
                            self.relations[prev_point] = []
                        
                        if prev_point not in self.relations[point]:
                            self.relations[point].append(prev_point)
                        
                    if next is not None:
                        next_point = Vector2(*next)
                        
                        if next_point not in self.relations:
                            self.relations[next_point] = []
                        
                        if next_point not in self.relations[point]:
                            self.relations[point].append(next_point)

                self.lines.append(Line(name_, coords_))

if __name__ == '__main__':
    location = Map('russas.geojson')