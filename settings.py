from rgb import hexToRGB, hexToRGBA

ZOOM_FACTOR = 0.1

LINE_WIDTH = 0.00005

CIRCLE_WIDTH = 0.0001
CIRCLE_SEGMENTS = 20

BG_COLOR = hexToRGBA('#555A60', 1)
LINE_COLOR = hexToRGB('#353C42')

POLYGON_COLOR = {
    'grass': hexToRGB('#6A807C'),
    'water': hexToRGB('#6A7780'),
    'building': hexToRGB('#464B51'),
    'other': hexToRGB('#51555C'),
}

PATH_COLOR = hexToRGB('#0EE1FA')