from math import radians, sin, cos
from json import loads

from vec import Vec2

from settings import LINE_WIDTH, CIRCLE_WIDTH, CIRCLE_SEGMENTS

class Point:
    def __init__(self, coord: Vec2):
        self.coord = coord
        
        self.triangles = self.transform()
        
    def transform(self):
        w = CIRCLE_WIDTH / 2
        step = 360 / CIRCLE_SEGMENTS
        
        lines: list[Vec2] = []
        
        for i in range(CIRCLE_SEGMENTS):
            angle = i * step
            
            x = self.coord.x + w * cos(radians(angle))
            y = self.coord.y + w * sin(radians(angle))
            
            lines.append(Vec2(x, y))
        
        triangles: list[Vec2] = []
        
        for curr, next in zip(lines, lines[1:] + [lines[0]]):
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

        triangles: list[Vec2] = []
        
        for curr, next in zip(lines[:-1], lines[1:]):
            triangles.extend([curr[0], curr[1],  next[0]])
            triangles.extend([next[0], next[1], curr[1]])

        return triangles
    
class Polygon:
    def __init__(self, type: str, coords: list[list[Vec2]]):
        self.type = type
        self.coords = coords
        
        self.triangles = self.transform()
    
    def transform(self):
        triangles: list[list[Vec2]] = []
        
        for coord in self.coords:
            triangles.append(self.triangulate(coord))
        
        return triangles
        
    def triangulate(self, coord: list[Vec2]):
        triangles: list[Vec2] = []

        if self.isClockwise(coord):
            coord = coord[::-1]
        else:
            coord = coord[:]

        while len(coord) >= 3:
            a = self.getEar(coord)
            if a == []:
                break

            triangles.extend(a)
        return triangles

    def isClockwise(self, coord: list[Vec2]):
        # initialize sum with last element
        sum = (coord[0].x - coord[len(coord) - 1].x) * (coord[0].y + coord[len(coord) - 1].y)

        # iterate over all other elements (0 to n-1)
        for i in range(len(coord) - 1):
            sum += (coord[i + 1].x - coord[i].x) * (coord[i + 1].y + coord[i].y)

        return sum > 0

    def getEar(self, coord: list[Vec2]):
        size = len(coord)

        if size < 3:
            return []

        if size == 3:
            tri = [coord[0], coord[1], coord[2]]
            del coord[:]
            return tri

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
        # only convex if traversing anti-clockwise!
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

        self.points: list[Point] = []
        self.line_strings: list[LineString] = []
        
        self.polygons: dict['str', list[Polygon]] = { 
            'other': [], 'building': [], 'water': [], 'grass': [],
        }
        
        self.graph: dict[Vec2, list[Vec2]] = {}
        
        self.start: Point | None = None
        self.goal: Point | None = None
        
        self.path: LineString | None = None
        self.distance: float = 0

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
                    if properties.get('type') == 'boundary' or properties.get('barrier'):
                        continue
                        
                    if properties.get('landuse') in (
                        'forest', 'allotments', 'meadow', 'cemetery', 'grass',
                    ) or properties.get('natural') in (
                        'grassland', 'heath', 'scrub', 'wood', 'wetland',
                    ) or properties.get('leisure') == 'park':
                        type_ = 'grass'
                    
                    elif properties.get('leisure') in (
                        'swimming_pool',
                    ) or properties.get('natural') in (
                        'water',
                    ):
                        type_ = 'water'
                    
                    elif properties.get('building'):
                        type_ = 'building'
                        
                    else:
                        type_ = 'other'
                    
                    coords_ = [[Vec2(*point) for point in coord] for coord in coords]
                    
                    self.polygons[type_].append(Polygon(type_, coords_))
                    
                    for coord_ in coords_:
                        self.min = Vec2.min(self.min, *coord_)
                        self.max = Vec2.max(self.max, *coord_)
    
    def select(self, coord: Vec2):
        coord = coord.nearest(list(self.graph.keys()))
        
        self.path = None
        self.distance = 0
        
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
            self.loadPath()
        
    def loadPath(self):
        start = self.start.coord
        goal = self.goal.coord
        
        openSet = {start}

        cameFrom = {}

        gScore: dict[Vec2, float] = {start: 0}
        fScore = {start: Vec2.distance(start, goal)}

        while len(openSet) > 0:
            current = min(openSet, key=lambda x: fScore[x])

            if current == goal:
                total_path = [current]

                while current in cameFrom:
                    current = cameFrom[current]
                    total_path.append(current)

                self.path = LineString(total_path)
                self.distance = gScore[goal]
                
                return

            openSet.remove(current)

            for neighbor in self.graph[current]:
                tentative_gScore = gScore[current] + Vec2.haversine(current, neighbor)

                if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + Vec2.distance(neighbor, goal)

                    if neighbor not in openSet:
                        openSet.add(neighbor)

        self.path = None
        self.distance = 0
        
if __name__ == '__main__':
    location = Map('russas.geojson')