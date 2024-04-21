from json import loads
from typing import Callable
from math import cos, sin, radians

from settings import *
from vec import Vec2

class Point:
    def __init__(self, map: 'Map', coord: Vec2):
        self.map = map
        self.coord = coord
        
        self.triangles = self.transform()
        
    def transform(self):
        w = POINT_WIDTH / (2 * (self.map.max.x - self.map.min.x))
        
        step = 360 / POINT_SEGMENTS
        
        points: list[Vec2] = []
        
        for i in range(POINT_SEGMENTS):
            angle = i * step
            
            x = self.coord.x + w * cos(radians(angle))
            y = self.coord.y + w * sin(radians(angle))
            
            points.append(Vec2(x, y))
        
        triangles: list[Vec2] = []
        
        for curr, next in zip(points, points[1:] + [points[0]]):
            triangles.append(self.coord)
            triangles.extend([curr, next])
        
        return triangles
    
class LineString:
    def __init__(self, map: 'Map', coords: list[Vec2]):
        self.map = map
        self.coords = coords
        
        self.triangles = self.transform()
    
    def transform(self):
        w = LINE_STRING_WIDTH / (2 * (self.map.max.x - self.map.min.x))
        
        lines: list[list[Vec2]] = []

        for prev, curr, next in zip([None] + self.coords[:-1], self.coords, self.coords[1:] + [None]):
            t0 = Vec2(0, 0) if prev is None else (curr - prev).normalize()
            t1 = Vec2(0, 0) if next is None else (next - curr).normalize()
            
            n0 = Vec2(-t0.y, t0.x)
            n1 = Vec2(-t1.y, t1.x)
            
            if prev is None:
                lines.append([
                    curr + n1 * w,
                    curr - n1 * w,
                ])
                 
            elif next is None:
                lines.append([
                    curr + n0 * w,
                    curr - n0 * w,
                ])
            else: 
                m = (n0 + n1).normalize()
                    
                dy = w / Vec2.dot(m, n1)
                
                lines.append([
                    curr + m * dy,
                    curr - m * dy,
                ])

        triangles: list[Vec2] = []
        
        for curr, next in zip(lines[:-1], lines[1:]):
            triangles.extend([curr[0], curr[1],  next[0]])
            triangles.extend([next[0], next[1], curr[1]])

        return triangles

class Text:
    def __init__(self, value: str, coord: Vec2, max_width: float):
        self.value = value
        self.coord = coord
        self.max_width = max_width
    
class Polygon:
    def __init__(self, coords: list[Vec2]):
        self.coords = coords
        
        self.triangles = self.transform()
    
    def transform(self):
        triangles: list[Vec2] = []

        if self.isClockwise(self.coords):
            coords = self.coords[::-1]
        else:
            coords = self.coords[:]

        while len(coords) >= 3:
            a = self.getEar(coords)
            if a == []:
                break

            triangles.extend(a)
        return triangles


    def isClockwise(self, coord: list[Vec2]):
        sum = (coord[0].x - coord[len(coord) - 1].x) * (coord[0].y + coord[len(coord) - 1].y)

        for i in range(len(coord) - 1):
            sum += (coord[i + 1].x - coord[i].x) * (coord[i + 1].y + coord[i].y)

        return sum > 0

    def getEar(self, coord: list[Vec2]):
        size = len(coord)

        if size < 3:
            return []

        if size == 3:
            triangle = [coord[0], coord[1], coord[2]]
            del coord[:]
            return triangle

        for i in range(size):
            tritest = False

            p1 = coord[(i - 1) % size]
            p2 = coord[i % size]
            p3 = coord[(i + 1) % size]

            if self.isConvex(p1, p2, p3):
                for x in coord:
                    if not (x in (p1, p2, p3)) and self.isInTriangle(p1, p2, p3, x):
                        tritest = True

                if tritest == False:
                    del coord[i % size]
                    return [p1, p2, p3]
        return []

    def isConvex(self, a: Vec2, b: Vec2, c: Vec2):
        crossp = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

        if crossp >= 0:
            return True

        return False

    def isInTriangle(self, a: Vec2, b: Vec2, c: Vec2, p: Vec2):
        return (c.x - p.x) * (a.y - p.y) - (a.x - p.x) * (c.y - p.y) >= 0 and \
                (a.x - p.x) * (b.y - p.y) - (b.x - p.x) * (a.y - p.y) >= 0 and \
                (b.x - p.x) * (c.y - p.y) - (c.x - p.x) * (b.y - p.y) >= 0

class Map:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
        # BOX LIMITS
        self.min = Vec2(float('inf'), float('inf'))
        self.max = Vec2(float('-inf'), float('-inf'))
        
        # VIEW
        self.scale = 1.0
        self.offset = Vec2(0, 0)
        
        # FIXED ELEMENTS
        self.line_strings: list[LineString] = []
        self.texts: list[Text] = []
        self.polygons: dict[str, list[Polygon]] = { 
            'other': [], 'building': [], 'water': [], 'grass': []
        }
        
        # GRAPH
        self.graph: dict[Vec2, list[Vec2]] = {}
        
        # DINAMIC ELEMENTS
        self.start: Point | None = None
        self.goal: Point | None = None
        self.path: LineString | None = None
        
        # DISTANCE
        self.distance = 0.0
        
        self.load()
        
    def load(self):
        with open(self.filepath, 'r') as f:
            data = loads(f.read())
        
        for feature in data['features']:
            geometry_type = feature['geometry']['type']
            geometry_coords = feature['geometry']['coordinates']
            
            if geometry_type == 'LineString':
                coords = [Vec2(*coord) for coord in geometry_coords]
            elif geometry_type == 'Polygon':
                coords = [Vec2(*coord) for coord in geometry_coords[0]]
            else:
                continue
            
            self.min = Vec2.min(self.min, *coords)
            self.max = Vec2.max(self.max, *coords)
        
        for feature in data['features']:
            properties = feature['properties']
            
            geometry_coords = feature['geometry']['coordinates']
            geometry_type = feature['geometry']['type']
            
            if geometry_type == 'LineString':
                if properties.get('highway') not in (
                    'motorway', 
                    'motorway_link', 
                    'trunk', 
                    'trunk_link',
                    'primary',
                    'primary_link',
                    
                    'secondary',
                    'secondary_link',
                    'tertiary',
                    'tertiary_link',
                    'road',
                    
                    'living_street',
                    'pedestrian',
                    'unclassified',
                    'residential',
                ):
                    continue
                
                coords = [self.normalize(Vec2(*coord)) for coord in geometry_coords]                        
                
                self.line_strings.append(LineString(self, coords))
                
                for prev, curr, next in zip([None] + coords[:-1], coords, coords[1:] + [None]):
                    if curr not in self.graph:
                        self.graph[curr] = []
                        
                    if prev and prev not in self.graph[curr]:
                        self.graph[curr].append(prev)
                
                    if next and next not in self.graph[curr]:
                        self.graph[curr].append(next)
                
            elif geometry_type == 'Polygon':
                if properties.get('type') == 'boundary':
                    continue
                
                if properties.get('landuse') in (
                    'forest', 
                    'allotments', 
                    'meadow', 
                    'cemetery', 
                    'grass'
                ) or properties.get('natural') in (
                    'grassland', 
                    'heath', 
                    'scrub', 
                    'wood',
                    'wetland'
                ) or properties.get('leisure') == 'park':
                    type = 'grass'
                
                elif properties.get('leisure') == 'swimming_pool' or \
                    properties.get('natural') == 'water':
                    type = 'water'
            
                elif properties.get('building') is not None:
                    type = 'building'
                
                else:
                    type = 'other'
                
                coords = [self.normalize(Vec2(*coord)) for coord in geometry_coords[0]]
                
                self.polygons[type].append(Polygon(coords))
                
                name = properties.get('name')
                
                if name is None:
                    continue
                
                min = Vec2.min(*coords)
                max = Vec2.max(*coords)
                
                width = max.x - min.x
                center = (min + max) / 2
                
                self.texts.append(Text(name, center, width))
                
            else:
                continue

    def normalize(self, coord: Vec2):
        return ((coord - self.min) / (self.max - self.min)) * 2 - 1

    def original(self, coord: Vec2):
        return ((coord + 1) / 2) * (self.max - self.min) + self.min
      
    def zoom(self, coord: Vec2, sign: float):
        scale = self.scale * (1 + ZOOM_FACTOR) ** sign
        
        self.offset -= (scale - self.scale) * coord
        self.scale = scale
        
    def move(self, movement: Vec2):
        self.offset -= movement * self.scale
 
    def select(self, coord: Vec2):
        coord = coord.nearest(self.graph.keys())
        
        self.path = None
        self.distance = 0.0
        
        if self.start is None:
            self.start = Point(self, coord)
            
        elif self.start.coord == coord:
            self.start = None
            
            if self.goal is not None:
                self.start, self.goal = self.goal, self.start
                
        elif self.goal is None or self.goal.coord != coord:
            self.goal = Point(self, coord)
            
        elif self.goal.coord == coord:
            self.goal = None
            
        if self.start is not None and self.goal is not None:
            path, distance = self.construct_path()
            
            coords = [self.normalize(item) for item in path]
            
            self.path = LineString(self, coords)
            self.distance = distance
            
            print(distance)
 
    def construct_path(self):
        start = self.original(self.start.coord)
        goal = self.original(self.goal.coord)
        
        openSet = { start }

        cameFrom = {}

        gScore: dict[Vec2, float] = { start: 0 }
        fScore = { start: Vec2.distance(start, goal) }

        while len(openSet) > 0:
            current = min(openSet, key=lambda x: fScore[x])

            if current == goal:
                path = [current]

                while current in cameFrom:
                    current = cameFrom[current]
                    path.append(current)
                
                return path, gScore[goal]

            openSet.remove(current)

            for neighbor in self.graph[self.normalize(current)]:
                neighbor = self.original(neighbor)
                
                tentative_gScore = gScore[current] + Vec2.haversine(current, neighbor)

                if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + Vec2.distance(neighbor, goal)

                    if neighbor not in openSet:
                        openSet.add(neighbor)

        return [], 0.0

if __name__ == '__main__':
    m = Map('russas.geojson')