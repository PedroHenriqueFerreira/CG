from typing import Any
from json import loads

from random import choice, random, randint

from structures.vector import Vec2

from objects.textures import Texture2D
from objects.sound import Sound
from objects.point import Point
from objects.text import Text
from objects.car import Car
from objects.button import Button

from objects.view import View
from objects.projection import Projection
from objects.light import Light

from objects.metrics import Metrics
from objects.polygons import Polygons
from objects.line_strings import LineStrings
from objects.textures import Textures
from objects.skybox import SkyBox
from objects.ground import Ground
from objects.shaders import Shaders

from settings import *

class Map:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
        self.metrics = Metrics(self)
        self.polygons = Polygons(self)
        self.line_strings = LineStrings(self)
        
        self.load()
        
        self.light = Light()
        self.view = View()
        self.projection = Projection()
        
        self.skybox = SkyBox(self)
        self.ground = Ground(self)

        self.shaders = Shaders(self)
        self.textures = Textures(self)

        #############

        # VIEW
        self.scale = 1.0
        
        self.rotation = Vec2(0, 0)
        self.offset = Vec2(0, 0)

        # GRAPH
        self.graph: dict[Vec2, list[Vec2]] = {}

        # SOUNDS
        self.sounds: dict[str, Sound] = {}

        # BUTTONS
        self.buttons: list[Button] = []

        # FIXED ELEMENTS
        self.texts: list[Text] = []

        # RANDOM ELEMENTS
        self.points: list[Point] = []
        self.cars: list[Car] = []

        # CONTROLLABLE ELEMENTS
        self.origin: Point | None = None
        self.destiny: Point | None = None
        self.my_car: Car | None = None

        # DISTANCE
        self.distance = 0.0


    def load(self):
        with open(self.filepath, 'r', encoding='utf8') as f:
            data = loads(f.read())

        self.metrics.load(data)
        self.polygons.load(data)
        self.line_strings.load(data)
        
    def load_sounds(self):
        self.sounds[FORWARD_SOUND_PATH] = Sound(FORWARD_SOUND_PATH)
        self.sounds[LEFT_SOUND_PATH] = Sound(LEFT_SOUND_PATH)
        self.sounds[RIGHT_SOUND_PATH] = Sound(RIGHT_SOUND_PATH)
        self.sounds[FINISH_SOUND_PATH] = Sound(FINISH_SOUND_PATH)
        
        self.sounds[POTHOLE_SOUND_PATH] = Sound(POTHOLE_SOUND_PATH)
        self.sounds[ACCIDENT_SOUND_PATH] = Sound(ACCIDENT_SOUND_PATH)
        self.sounds[POLICE_SOUND_PATH] = Sound(POLICE_SOUND_PATH)
        self.sounds[CAMERA_SOUND_PATH] = Sound(CAMERA_SOUND_PATH)

        self.sounds[RECALCULATE_SOUND_PATH] = Sound(RECALCULATE_SOUND_PATH)
        self.sounds[PILOT_ENABLE_SOUND_PATH] = Sound(PILOT_ENABLE_SOUND_PATH)
        self.sounds[PILOT_DISABLE_SOUND_PATH] = Sound(PILOT_DISABLE_SOUND_PATH)
        self.sounds[PILOT_UNAVAILABLE_SOUND_PATH] = Sound(PILOT_UNAVAILABLE_SOUND_PATH)
        self.sounds[CANCEL_SOUND_PATH] = Sound(CANCEL_SOUND_PATH)

    def load_buttons(self):
        self.buttons.append(
            Button(
                self,
                CANCEL_POS,
                self.textures[CANCEL_TEXTURE_PATH],
                self.textures[CANCEL_HOVER_TEXTURE_PATH],
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                self.cancel_path
            )
        )
        
        self.buttons.append(
            Button(
                self,
                PILOT_POS,
                self.textures[PILOT_TEXTURE_PATH],
                self.textures[PILOT_HOVER_TEXTURE_PATH],
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                self.pilot_path
            )
        )
        
        self.buttons.append(
            Button(
                self,
                RECALCULATE_POS,
                self.textures[RECALCULATE_TEXTURE_PATH],
                self.textures[RECALCULATE_HOVER_TEXTURE_PATH],
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                self.recalculate_path
            )
        )

    def cancel_path(self):
        self.origin = None
        self.destiny = None

        self.path = None
        self.distance = 0.0

        self.my_car = None

        self.buttons.clear()
        
        self.sounds[CANCEL_SOUND_PATH].play()
        
    def recalculate_path(self):
        if not self.my_car:
            return
        
        pos = self.my_car.pos.nearest(*self.graph.keys())
        
        self.load_origin(pos)
        
        self.load_my_car()
        self.load_path()
        
        self.sounds[RECALCULATE_SOUND_PATH].play()
    
    def pilot_path(self):
        if not self.my_car:
            return
        
        coords = self.path.coords
        
        pilot = self.my_car.pilot
        pos = self.my_car.pos
        prev_pos = self.my_car.prev_pos
        next_pos = self.my_car.next_pos
        
        if pilot:
            self.sounds[PILOT_DISABLE_SOUND_PATH].play()
            
            self.my_car.pilot = False
        else:
            if pos not in coords and (prev_pos not in coords or next_pos not in coords):
                self.sounds[PILOT_UNAVAILABLE_SOUND_PATH].play()
                
                return
            
            self.sounds[PILOT_ENABLE_SOUND_PATH].play()
            
            self.my_car.pilot = True
    
    def load_graph(self, coords: list[Vec2]):
        for prev, curr, next in zip([None] + coords[:-1], coords, coords[1:] + [None]):
            if curr not in self.graph:
                self.graph[curr] = []

            if prev and prev not in self.graph[curr]:
                self.graph[curr].append(prev)

            if next and next not in self.graph[curr]:
                self.graph[curr].append(next)

        return True

    def load_point(self, coords: list[Vec2]):
        if POINT_PROBABILITY < random():
            return False

        pos = choice(coords)

        match randint(0, 3):
            case 0:
                texture = self.textures[ACCIDENT_TEXTURE_PATH]
                sound = self.sounds[ACCIDENT_SOUND_PATH]
            case 1:
                texture = self.textures[CAMERA_TEXTURE_PATH]
                sound = self.sounds[CAMERA_SOUND_PATH]
            case 2:
                texture = self.textures[POLICE_TEXTURE_PATH]
                sound = self.sounds[POLICE_SOUND_PATH]
            case 3:
                texture = self.textures[POTHOLE_TEXTURE_PATH]
                sound = self.sounds[POTHOLE_SOUND_PATH]

        self.points.append(
            Point(
                self,
                pos,
                texture,
                POINT_SIZE,
                POINT_MIN_SIZE,
                POINT_MAX_SIZE,
                POINT_MAX_BLINK_SCALE,
                POINT_DELTA_BLINK_SCALE,
                POINT_MAX_BLINK_TIMES,
                sound
            )
        )

        return True

    def load_car(self, coords: list[Vec2]):
        if CAR_PROBABILITY < random():
            return False

        pos = choice(coords)

        match randint(0, 4):
            case 0:
                texture = self.textures[YELLOW_CAR_TEXTURE_PATH]
                circle_texture = self.textures[YELLOW_CAR_CIRCLE_TEXTURE_PATH]
            case 1:
                texture = self.textures[BLUE_CAR_TEXTURE_PATH]
                circle_texture = self.textures[BLUE_CAR_CIRCLE_TEXTURE_PATH]
            case 2:
                texture = self.textures[GREEN_CAR_TEXTURE_PATH]
                circle_texture = self.textures[GREEN_CAR_CIRCLE_TEXTURE_PATH]
            case 3:
                texture = self.textures[RED_CAR_TEXTURE_PATH]
                circle_texture = self.textures[RED_CAR_CIRCLE_TEXTURE_PATH]
            case 4:
                texture = self.textures[PURPLE_CAR_TEXTURE_PATH]
                circle_texture = self.textures[PURPLE_CAR_CIRCLE_TEXTURE_PATH]

        self.cars.append(
            Car(
                self,
                pos,
                True,
                texture,
                CAR_SIZE,
                circle_texture,
                CAR_CIRCLE_SIZE,
                CAR_CIRCLE_MIN_SIZE,
                CAR_CIRCLE_MAX_SIZE,
                CAR_FORWARD_SIZE,
                CAR_BACKWARD_SIZE,
                CAR_ROTATION_SIZE,
                self.sounds[FORWARD_SOUND_PATH],
                self.sounds[RIGHT_SOUND_PATH],
                self.sounds[LEFT_SOUND_PATH],
                self.sounds[FINISH_SOUND_PATH],
                
            )
        )

        return True

    def load_line_string_text(self, properties: dict, coords: list[Vec2]):
        name = properties.get('name')

        if not name:
            return False

        self.texts.append(
            Text(
                self,
                name,
                coords,
                LINE_STRING_TEXT_COLOR,
                LINE_STRING_TEXT_THICKNESS,
                LINE_STRING_TEXT_SIZE,
                LINE_STRING_TEXT_MIN_SIZE,
                LINE_STRING_TEXT_MAX_SIZE
            )
        )

        return True

    def load_polygon_text(self, properties: dict, coords: list[Vec2]):
        name = properties.get('name')

        if not name:
            return False

        min, max = Vec2.min(*coords), Vec2.max(*coords)

        y = (min.y + max.y) / 2

        west, east = Vec2(min.x, y), Vec2(max.x, y)

        self.texts.append(
            Text(
                self,
                name,
                [west, east],
                POLYGON_TEXT_COLOR,
                POLYGON_TEXT_THICKNESS,
                POLYGON_TEXT_SIZE,
                POLYGON_TEXT_MIN_SIZE,
                POLYGON_TEXT_MAX_SIZE
            )
        )

        return True

    def zoom(self, coord: Vec2, direction: float):
        scale = self.scale * ZOOM_FACTOR ** direction

        self.offset += (coord - self.offset) * (1 - (self.scale / scale))

        self.scale = scale

    def move(self, movement: Vec2):
        self.offset += movement

    def rotate(self, movement: Vec2):
        self.rotation = movement

    def load_origin(self, pos: Vec2):
        self.origin = Point(
            self,
            pos,
            self.textures[ORIGIN_TEXTURE_PATH],
            ORIGIN_SIZE,
            ORIGIN_MIN_SIZE,
            ORIGIN_MAX_SIZE,
            POINT_MAX_BLINK_SCALE,
            POINT_DELTA_BLINK_SCALE,
            POINT_MAX_BLINK_TIMES,
        )

    def load_destiny(self, pos: Vec2):
        self.destiny = Point(
            self,
            pos,
            self.textures[DESTINY_TEXTURE_PATH],
            DESTINY_SIZE,
            DESTINY_MIN_SIZE,
            DESTINY_MAX_SIZE,
            POINT_MAX_BLINK_SCALE,
            POINT_DELTA_BLINK_SCALE,
            POINT_MAX_BLINK_TIMES,
        )

    def load_path(self):
        origin = self.metrics.denormalize(self.origin.pos)
        destiny = self.metrics.denormalize(self.destiny.pos)

        openSet = {origin}

        cameFrom = {}

        gScore: dict[Vec2, float] = { origin: 0 }
        fScore = {origin: Vec2.distance(origin, destiny)}

        while len(openSet) > 0:
            current = min(openSet, key=lambda x: fScore[x])

            if current == destiny:
                path = [current]

                while current in cameFrom:
                    current = cameFrom[current]
                    path.append(current)

                path.reverse()
                
                coords = [self.metrics.normalize(coord) for coord in path]

                self.my_car.rotate(Vec2.angle(self.my_car.j, coords[1] - coords[0]))
                
                self.line_strings.create_path(coords)
                
                self.distance = gScore[destiny]

                return

            openSet.remove(current)

            for neighbor in self.graph[self.metrics.normalize(current)]:
                neighbor = self.metrics.denormalize(neighbor)

                tentative_gScore = gScore[current] + \
                    Vec2.haversine(current, neighbor)

                if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + \
                        Vec2.distance(neighbor, destiny)

                    if neighbor not in openSet:
                        openSet.add(neighbor)

    def load_my_car(self):
        self.my_car = Car(
            self,
            self.origin.pos,
            False,
            self.textures[WHITE_CAR_TEXTURE_PATH],
            MY_CAR_SIZE,
            self.textures[WHITE_CAR_CIRCLE_TEXTURE_PATH],
            MY_CAR_CIRCLE_SIZE,
            MY_CAR_CIRCLE_MIN_SIZE,
            MY_CAR_CIRCLE_MAX_SIZE,
            CAR_FORWARD_SIZE,
            CAR_BACKWARD_SIZE,
            CAR_ROTATION_SIZE,
            self.sounds[FORWARD_SOUND_PATH],
            self.sounds[RIGHT_SOUND_PATH],
            self.sounds[LEFT_SOUND_PATH],
            self.sounds[FINISH_SOUND_PATH]
        )

    def nearest(self, pos: Vec2, node: Vec2 | None = None):
        if node is None:
            node = pos.nearest(*self.graph.keys())
        
        closest = node
        closest_distance = Vec2.distance(pos, node)
        factor = 0.01
        
        for neighbor in self.graph[node]:
            relation = neighbor - node
            
            current_factor = 0
            
            current_closest_distance = float('inf')
            
            while current_factor <= 1:
                next = node + relation * current_factor
                next_distance = Vec2.distance(pos, next)
                
                if next_distance < current_closest_distance:
                    current_closest_distance = next_distance
                else:
                    break

                if next_distance < closest_distance:
                    closest_distance = next_distance
                    closest = next
                
                current_factor += factor
            
        return closest

    def select(self, pos: Vec2):
        pos = pos.nearest(*self.graph.keys())
        # pos = self.nearest(pos)
    
        self.path = None

        if not self.origin:
            self.load_origin(pos)
    
        elif self.origin.pos != pos:
            self.load_destiny(pos)

        else:
            self.origin = None

        if self.origin and self.destiny:
            self.load_my_car()
            self.load_path()
            
            self.load_buttons()

    def hover(self, pos: Vec2):
        for button in self.buttons:
            button.hover(pos)
