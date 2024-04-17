from json import loads
from typing import Callable
from math import cos, sin, radians

from settings import *
from vec import Vec2

class Point:
    def __init__(self, coord: Vec2):
        self.coord = coord
        
        self.triangles = self.transform()
        
    def transform(self):
        w = POINT_WIDTH / 2
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
    def __init__(self, coords: list[Vec2]):
        self.coords = coords
        
        self.triangles = self.transform()
    
    def transform(self):
        w = LINE_WIDTH / 2
        
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
    
class Polygon:
    def __init__(self, name: str | None, coords: list[Vec2]):
        self.name = name
        self.coords = coords
        
        self.min = Vec2.min(*self.coords)
        self.max = Vec2.max(*self.coords)
        self.center = Vec2.center(*self.coords)
        
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
        self.global_min = Vec2(float('inf'), float('inf'))
        self.global_max = Vec2(float('-inf'), float('-inf'))
        
        # VISIBLE BOX
        self.min = Vec2(float('inf'), float('inf'))
        self.max = Vec2(float('-inf'), float('-inf'))
        
        # OBJECTS
        self.line_strings: list[LineString] = []
        self.polygons: dict[str, list[Polygon]] = { 
            'other': [], 'building': [], 'water': [], 'grass': []
        }
        
        # GRAPH
        self.graph: dict[Vec2, list[Vec2]] = {}
        
        # PATH
        self.start: Point | None = None
        self.goal: Point | None = None
        self.path: LineString | None = None
        self.distance = 0.0
        
        self.load()
        
    def load(self):
        with open(self.filepath, 'r') as f:
            data = loads(f.read())
            
        for feature in data['features']:
            properties = feature['properties']
            coords = feature['geometry']['coordinates']
            
            type = feature['geometry']['type']
            
            if type == 'LineString':
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
                    
                coords_ = [Vec2(*coord) for coord in coords]
                
                for prev, curr, next in zip([None] + coords_[:-1], coords_, coords_[1:] + [None]):
                    if curr not in self.graph:
                        self.graph[curr] = []
                        
                    if prev and prev not in self.graph[curr]:
                        self.graph[curr].append(prev)
                
                    if next and next not in self.graph[curr]:
                        self.graph[curr].append(next)
                        
                self.line_strings.append(LineString(coords_))
                
                
            elif type == 'Polygon':
                if properties.get('type') == 'boundary':
                    continue
                
                name_ = properties.get('name')
                
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
                    type_ = 'grass'
                
                elif properties.get('leisure') == 'swimming_pool' or properties.get('natural') == 'water':
                    type_ = 'water'
            
                elif properties.get('building') is not None:
                    type_ = 'building'
                
                else:
                    type_ = 'other'
                
                coords_ = [Vec2(*coord) for coord in coords[0]]
                
                self.polygons[type_].append(Polygon(name_, coords_))
                
            else:
                continue
                
            self.global_min = Vec2.min(self.global_min, *coords_)
            self.global_max = Vec2.max(self.global_max, *coords_)

        self.min = self.global_min
        self.max = self.global_max

    def select(self, coord: Vec2):
        coord = coord.nearest(self.graph.keys())
        
        self.path = None
        self.distance = 0.0
        
        if self.start is None:
            self.start = Point(coord)
        elif self.start.coord == coord:
            self.start = None
        elif self.goal is None or self.goal.coord != coord:
            self.goal = Point(coord)
        elif self.goal.coord == coord:
            self.goal = None
            
        if self.start is None and self.goal is not None:
            self.start, self.goal = self.goal, self.start
            
        if self.start is not None and self.goal is not None:
            path, distance = self.a_star(self.start.coord, self.goal.coord, Vec2.distance)
            
            self.path = LineString(path)
            self.distance = distance
        
    def zoom(self, coord: Vec2, sign: float):
        factor = sign * ZOOM_FACTOR
        
        self.min += (coord - self.min) * factor
        self.max -= (self.max - coord) * factor
        
    def move(self, movement: Vec2):
        self.min -= movement
        self.max -= movement

    def a_star(self, start: Vec2, goal: Vec2, h: Callable[[Vec2, Vec2], float]):
        openSet = { start }

        cameFrom = {}

        gScore: dict[Vec2, float] = { start: 0 }
        fScore = { start: h(start, goal) }

        while len(openSet) > 0:
            current = min(openSet, key=lambda x: fScore[x])

            if current == goal:
                total_path = [current]

                while current in cameFrom:
                    current = cameFrom[current]
                    total_path.append(current)
                
                return total_path, gScore[goal]

            openSet.remove(current)

            for neighbor in self.graph[current]:
                tentative_gScore = gScore[current] + Vec2.haversine(current, neighbor)

                if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + h(neighbor, goal)

                    if neighbor not in openSet:
                        openSet.add(neighbor)

        return [], 0.0

if __name__ == '__main__':
    m = Map('russas.geojson')