from typing import Any
from json import loads

from random import choice, random

from structures.vector import Vec2

from objects.line_string import LineString
from objects.polygon import Polygon
from objects.point import Point
from objects.car import Car

from settings import ZOOM_FACTOR

class Map:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
        # BOX LIMITS
        self.min = Vec2(float('inf'), float('inf'))
        self.max = Vec2(float('-inf'), float('-inf'))
        
        # VIEW
        self.scale = 1.0
        self.offset = Vec2(0, 0)
        
        # ELEMENTS
        self.line_strings: dict[str, list[LineString]] = {}
        self.polygons: dict[str, list[Polygon]] = {}
        self.points: dict[str, list[Point]] = {}
        
        self.car = Car()
        
        # GRAPH
        self.graph: dict[Vec2, list[Vec2]] = {}
        
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
            properties: dict[str, Any] = feature['properties']
            
            geometry_coords = feature['geometry']['coordinates']
            geometry_type = feature['geometry']['type']
            
            if geometry_type == 'LineString':
                if properties.get('highway') in ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link'):
                    type = 'primary'
                
                elif properties.get('highway') in ('secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'road'):
                    type = 'secondary'
                
                elif properties.get('highway') in ('living_street', 'pedestrian', 'unclassified', 'residential'):
                    type = 'tertiary'
                
                else:
                    continue
                
                name = properties.get('name', '')
                coords = [self.normalize(Vec2(*coord)) for coord in geometry_coords]                        
                
                if type not in self.line_strings:
                    self.line_strings[type] = []
                
                self.line_strings[type].append(LineString(name, coords))
                
                # RANDOM POINTS
                if random() < 0.2:
                    types = ['hole', 'police', 'accident', 'camera']
                    
                    type = choice(types)
                    name = ['Buraco', 'Polícia', 'Acidente', 'Camera'][types.index(type)]
                    
                    if type not in self.points:
                        self.points[type] = []
                    
                    self.points[type].append(Point(name, choice(coords)))
                
                # UPDATE GRAPH
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
                
                if properties.get('landuse') in ('forest', 'allotments', 'meadow', 'cemetery', 'grass') or \
                    properties.get('natural') in ('grassland', 'heath', 'scrub', 'wood', 'wetland') or \
                    properties.get('leisure') == 'park':
                    type = 'grass'
                
                elif properties.get('leisure') == 'swimming_pool' or properties.get('natural') == 'water':
                    type = 'water'
            
                elif properties.get('building') is not None:
                    type = 'building'
                
                else:
                    type = 'other'
                
                name = properties.get('name', '')
                coords = [self.normalize(Vec2(*coord)) for coord in geometry_coords[0]]
                
                if type not in self.polygons:
                    self.polygons[type] = []
                
                self.polygons[type].append(Polygon(name, coords))
                
            else:
                continue
            
        self.car.pos = list(self.graph.keys())[0]


    def normalize(self, coord: Vec2):
        return ((coord - self.min) / (self.max - self.min)) * 2 - 1

    def original(self, coord: Vec2):
        return ((coord + 1) / 2) * (self.max - self.min) + self.min
      
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
            
            self.line_strings['path'] = [LineString('Percurso', coords)]

            # CHANGE
            self.car.pos = start[0].coord

 
    def construct_path(self):
        start = self.original(self.points['start'][0].coord)
        goal = self.original(self.points['goal'][0].coord)
        
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
