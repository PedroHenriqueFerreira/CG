from rgb import hexToRGB

FPS = 60
SPEED = 0.00001
ROTATE_SPEED = 0.05

LINE_WIDTH = 0.00005

POINT_WIDTH = 0.0001
POINT_SEGMENTS = 8

ZOOM_FACTOR = 0.1

BG_COLOR = hexToRGB('#555A60')

LINE_STRING_COLOR = hexToRGB('#363D44')

POLYGON_COLOR = {
    'grass': hexToRGB('#526A64'),
    'water': hexToRGB('#526A7C'),
    'building': hexToRGB('#464B51'),
    'other': hexToRGB('#51565C'),
}

PATH_COLOR = hexToRGB('#04E5FE')

TEXT_COLOR = hexToRGB('#717983')