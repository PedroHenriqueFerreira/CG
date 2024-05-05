from typing import Any
from json import loads

from random import choice, random

from structures.vector import Vec2

from objects.line_string import LineString
from objects.polygon import Polygon
from objects.point import Point
from objects.text import Text
from objects.car import Car

from settings import ZOOM_FACTOR

class Map:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
        # BOX
        self.min = Vec2(float('inf'), float('inf'))
        self.max = Vec2(float('-inf'), float('-inf'))
        self.delta = Vec2(0, 0)
        
        # VIEW
        self.scale = 1.0
        self.offset = Vec2(0, 0)
        
        # GRAPH
        self.graph: dict[Vec2, list[Vec2]] = {}
        
        # FIXED ELEMENTS
        
        self.roads: list[LineString] = []
        
        self.greens: list[Polygon] = []
        self.waters: list[Polygon] = []
        self.buildings: list[Polygon] = []
        self.others: list[Polygon] = []
        
        self.texts: list[Text] = []
        
        # RANDOM ELEMENTS
        
        self.heavy_traffics: list[LineString] = []
        self.moderate_traffics: list[LineString] = []
        
        self.accidents: list[Point] = []
        self.cameras: list[Point] = []
        self.potholes: list[Point] = []
        self.cops: list[Point] = []
        
        self.cars: list[Car] = []
        
        # CUSTOM ELEMENTS
        
        self.path: LineString | None = None
        self.start: Point | None = None
        self.goal: Point | None = None
        self.car: Car | None = None
        
        # DISTANCE
        self.distance = 0.0
        
        self.load()
        
    def load(self):
        with open(self.filepath, 'r') as f:
            data = loads(f.read())
        
        self.load_box(data)
        self.load_elements(data)

    def load_box(self, data: dict):
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
        
        y = (self.min.y + self.max.y) / 2
        
        west = Vec2(self.min.x, y)
        east = Vec2(self.max.x, y)
        
        self.width = Vec2.haversine(west, east)

    def load_elements(self, data: dict):
        for feature in data['features']:
            properties: dict[str, Any] = feature['properties']
            
            geometry_coords = feature['geometry']['coordinates']
            geometry_type = feature['geometry']['type']
            
            self.load_points()
            
            if geometry_type == 'LineString':
                coords = [self.normalize(Vec2(*coord)) for coord in geometry_coords]
                       
                self.load_graph(coords)
                
                if self.load_line_string(properties, coords):
                    self.load_text(properties, coords)
                
            elif geometry_type == 'Polygon':
                coords = [self.normalize(Vec2(*coord)) for coord in geometry_coords[0]]
                
                if self.load_polygon(properties, coords):
                    min = Vec2.min(*coords)
                    max = Vec2.max(*coords)
                    
                    y = (min.y + max.y) / 2
                    
                    self.load_text(properties, [Vec2(min.x, y), Vec2(max.x, y)])
                
            else:
                continue

    def load_graph(self, coords: list[Vec2]):
        for prev, curr, next in zip([None] + coords[:-1], coords, coords[1:] + [None]):
            if curr not in self.graph:
                self.graph[curr] = []
            
            if prev and prev not in self.graph[curr]:
                self.graph[curr].append(prev)
        
            if next and next not in self.graph[curr]:
                self.graph[curr].append(next)

    def load_line_string(self, properties: dict, coords: list[Vec2]):
        if properties.get('highway') not in (
            'motorway', 'motorway_link', 'trunk', 
            'trunk_link', 'primary', 'primary_link',
            
            'secondary', 'secondary_link', 'tertiary', 
            'tertiary_link', 'road',
            
            'living_street', 'pedestrian', 'unclassified', 
            'residential',
        ):
            return False
        
        self.roads.append(LineString(self, coords))
        
        return True

    def load_polygon(self, properties: dict, coords: list[Vec2]):
        if properties.get('type') == 'boundary':
            return False
        
        polygon = Polygon(self, coords)
        
        if properties.get('landuse') in (
            'forest', 'allotments', 'meadow', 'grass'
        ) or properties.get('natural') in (
            'grassland', 'heath', 'scrub', 'wood', 'wetland'
        ) or properties.get('leisure') in (
            'park',
        ):
            self.greens.append(polygon)
        
        elif properties.get('leisure') in (
            'swimming_pool',
        ) or properties.get('natural') in (
            'water', 
        ):
            self.waters.append(polygon)
    
        elif properties.get('building'):
            self.buildings.append(polygon)

        else:
            self.others.append(polygon)

        return True

    def load_points(self): # TODO
        ...

    def load_text(self, properties: dict, coords: list[Vec2]):
        name = properties.get('name', '')
        
        if name == '':
            return
        
        self.texts.append(Text(self, name, coords))       

    def transform_km(self, size: float):
        delta = self.max - self.min
        aspect_ratio = delta.x / delta.y
        
        return size / self.width * aspect_ratio * 2

    def transform_pct(self, size: float):
        return size * 2

    def normalize(self, coord: Vec2):
        delta = self.max - self.min
        aspect_ratio = delta / delta.y
        
        return (((coord - self.min) / delta) * 2 - 1) * aspect_ratio

    def denormalize(self, coord: Vec2):
        delta = self.max - self.min
        aspect_ratio = delta / delta.y
        
        return ((coord / aspect_ratio + 1) / 2) * delta + self.min
      
    def zoom(self, coord: Vec2, direction: float):
        scale = self.scale * (1 + ZOOM_FACTOR) ** direction
        
        self.offset += (coord - self.offset) * (1 - (self.scale / scale))    
        
        self.scale = scale
        
    def move(self, movement: Vec2):
        self.offset += movement
 
    def select(self, coord: Vec2):
        coord = coord.nearest(self.graph.keys())
        
        self.line_strings['path'] = []
        
        start = self.points.get('start', [])
        goal = self.points.get('goal', [])
        
        if len(start) == 0:
            self.points['start'] = [Point('Origem', coord)]
            
        elif start[0].coord == coord:
            self.points['start'] = []
            
            if len(goal) > 0:
                self.points['start'], self.points['goal'] = self.points['goal'], self.points['start']
            
        elif len(goal) == 0 or goal[0].coord != coord:
            self.points['goal'] = [Point('Destino', coord)]
            
        elif goal[0].coord == coord:
            self.points['goal'] = []
            
        start = self.points.get('start', [])
        goal = self.points.get('goal', [])
            
        if len(start) > 0 and len(goal) > 0:
            path, distance = self.construct_path()
            
            coords = [self.normalize(point) for point in path]
            
            self.line_strings['path'] = [LineString(self,'Percurso', coords)]
            self.distance = distance

            # CHANGE
            self.car.pos = start[0].coord
            self.car.rotate(Vec2.degrees(self.car.j, coords[1] - coords[0]))

    def construct_path(self):
        start = self.denormalize(self.points['start'][0].coord)
        goal = self.denormalize(self.points['goal'][0].coord)
        
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
                
                return reversed(path), gScore[goal]

            openSet.remove(current)

            for neighbor in self.graph[self.normalize(current)]:
                neighbor = self.denormalize(neighbor)
                
                tentative_gScore = gScore[current] + Vec2.haversine(current, neighbor)

                if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + Vec2.distance(neighbor, goal)

                    if neighbor not in openSet:
                        openSet.add(neighbor)

        return [], 0.0
