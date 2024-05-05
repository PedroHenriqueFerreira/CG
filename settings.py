from rgb import hex_to_RGB

MAP_PATH = 'maps/russas.geojson'

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

ZOOM_FACTOR = 0.1

FPS = 60

CAR_TEXTURE = 'textures/car.png'
CAR_FORWARD_SPEED = 0.0015
CAR_BACKWARD_SPEED = 0.00075
CAR_ROTATION_SPEED = 0.01
CAR_WIDTH = 0.005

BG_COLOR = hex_to_RGB('#555A60')

GREEN_COLOR = hex_to_RGB('#527C6D')
WATER_COLOR = hex_to_RGB('#516C7D')
BUILDING_COLOR = hex_to_RGB('#464B51')
OTHER_COLOR = hex_to_RGB('#51565C')

LINE_STRING_SIZE = 0.006 # IN KM
LINE_STRING_SEGMENTS = 30 # IN INT

TEXT_SIZE = 0.015 # IN %
TEXT_MIN_SIZE = 0.002 # IN KM

ROAD_COLOR = hex_to_RGB('#363D44')
PATH_COLOR = hex_to_RGB('#04E5FE')

LINE_STRING_COLOR = {
    'path': hex_to_RGB('#04E5FE'),
    'road': hex_to_RGB('#363D44'),
}

POINT_WIDTH = 0.005

POINT_TEXTURE = {
    'start': 'textures/start.png',
    'goal': 'textures/goal.png',
    'pothole': 'textures/pothole.png',
    'cop': 'textures/cop.png',
    'camera': 'textures/camera.png',
    'accident': 'textures/accident.png',
}

TEXT_COLOR = hex_to_RGB('#AAAAAA')