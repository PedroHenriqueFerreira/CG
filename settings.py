from rgb import hexToRGB, hexToRGBA

ZOOM_FACTOR = 0.1

LINE_WIDTH = 0.00005

CIRCLE_WIDTH = 0.0001
CIRCLE_SEGMENTS = 20

BG_COLOR = hexToRGBA('#F8F7F7', 1)
LINE_COLOR = hexToRGB('#AAB9C9')

POLYGON_COLOR = {
    'grass': hexToRGB('#D3F8E2'),
    'pitch': hexToRGB('#A0F0C1'),
    'water': hexToRGB('#9CEAFF'),
    'building': hexToRGB('#E8E9ED'),
    'other': hexToRGB('#F5F0E5'),
}

POLYGON_BORDER_COLOR = {
    'grass': hexToRGB('#C8ECD7'),
    'pitch': hexToRGB('#98E4B7'),
    'water': hexToRGB('#94DEF2'),
    'building': hexToRGB('#DCDDE1'),
    'other': hexToRGB('#E9E4DA'),
}

PATH_COLOR = hexToRGB('#FF1EB2')