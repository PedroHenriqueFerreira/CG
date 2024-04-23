from rgb import hex_to_RGB

MAP_PATH = 'assets/russas.geojson'

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

ZOOM_FACTOR = 0.1

FPS = 60

CAR_TEXTURE = 'assets/car.png'
CAR_FORWARD_SPEED = 0.0025
CAR_BACKWARD_SPEED = 0.001
CAR_ROTATION_SPEED = 0.01
CAR_WIDTH = 0.005

BG_COLOR = hex_to_RGB('#555A60')

POLYGON_COLOR = {
    'grass': hex_to_RGB('#527C6D'),
    'water': hex_to_RGB('#516C7D'),
    'building': hex_to_RGB('#464B51'),
    'other': hex_to_RGB('#51565C'),
}

LINE_STRING_WIDTH = 0.005
LINE_STRING_COLOR = {
    'path': hex_to_RGB('#04E5FE'),
    'primary': hex_to_RGB('#2B2F34'),
    'secondary': hex_to_RGB('#2E3338'),
    'tertiary': hex_to_RGB('#363D44'),
}

POINT_WIDTH = 0.005
POINT_SEGMENTS = 24
POINT_COLOR = {
    'start': hex_to_RGB('#85F2FF'),
    'goal': hex_to_RGB('#85F2FF'),
    'hole': hex_to_RGB('#FE0760'),
    'blitz': hex_to_RGB('#FEB907'),
    'sensor': hex_to_RGB('#3300FF'),
}

TEXT_COLOR = hex_to_RGB('#AAAAAA')