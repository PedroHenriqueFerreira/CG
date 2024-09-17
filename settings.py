from structures.vector import Vec2
from objects.color import Color

from objects.texture import Texture2D

# GENERAL
BG_COLOR = Color.hex('#555A60')

WINDOW_WIDTH = 800 # IN PIXELS
WINDOW_HEIGHT = 800 # IN PIXELS

FPS = 60 # IN INTEGER

ZOOM_FACTOR = 1.1 # IN PERCENTAGE

CIRCLE_SEGMENTS = 30 # IN INTEGER

# LINE STRINGS 
LINE_STRING_SIZE = 0.006 # IN KILOMETERS
LINE_STRING_COLOR = Color.hex('#363D44')

LINE_STRING_TEXT_THICKNESS = 2 # IN INTEGER
LINE_STRING_TEXT_SIZE = 0.015 # IN PERCENTAGE
LINE_STRING_TEXT_MIN_SIZE = 0.002 # IN KILOMETERS
LINE_STRING_TEXT_MAX_SIZE = 0.012 # IN KILOMETERS
LINE_STRING_TEXT_COLOR = Color.hex('#AAAAAA')

PATH_SIZE = 0.006 # IN KILOMETERS
# PATH_COLOR = Color.hex('#04E5FE')
PATH_COLOR = Color.hex('#FFFFFF')

# POLYGONS
POLYGON_TEXT_THICKNESS = 2 # IN INTEGER
POLYGON_TEXT_SIZE = 0.018 # IN PERCENTAGE
POLYGON_TEXT_MIN_SIZE = 0.0024 # IN KILOMETERS
POLYGON_TEXT_MAX_SIZE = 0.015 # IN KILOMETERS
POLYGON_TEXT_COLOR = Color.hex('#AAAAAA')

# GRASS_COLOR = Color.hex('#527C6D')
# WATER_COLOR = Color.hex('#516C7D')
# BUILDING_COLOR = Color.hex('#464B51')
# UNKNOWN_COLOR = Color.hex('#51565C')

GRASS_COLOR = Color.hex('#FFFFFF')
WATER_COLOR = Color.hex('#FFFFFF')
BUILDING_COLOR = Color.hex('#FFFFFF')
UNKNOWN_COLOR = Color.hex('#FFFFFF')


# POINTS
POINT_SIZE = 0.03 # IN PERCENTAGE
POINT_MIN_SIZE = 0.006 # IN KILOMETERS
POINT_MAX_SIZE = 0.1 # IN KILOMETERS

POINT_MAX_BLINK_SCALE = 2 # IN PERCENTAGE
POINT_DELTA_BLINK_SCALE = 0.1 # IN PERCENTAGE
POINT_MAX_BLINK_TIMES = 5 # IN INTEGER

ORIGIN_SIZE = 0.03 # IN PERCENTAGE
ORIGIN_MIN_SIZE = 0.006 # IN KILOMETERS
ORIGIN_MAX_SIZE = 0.2 # IN KILOMETERS

DESTINY_SIZE = 0.03 # IN PERCENTAGE
DESTINY_MIN_SIZE = 0.006 # IN KILOMETERS
DESTINY_MAX_SIZE = 0.2 # IN KILOMETERS

POINT_PROBABILITY = 0.05 # IN PERCENTAGE

# CARS
CAR_SIZE = 0.006 # IN KILOMETERS
CAR_CIRCLE_SIZE = 0.0 # IN PERCENT
CAR_CIRCLE_MIN_SIZE = 0.024 # IN KILOMETERS
CAR_CIRCLE_MAX_SIZE = 0.3 # IN KILOMETERS

MY_CAR_SIZE = 0.006 # IN KILOMETERS
MY_CAR_CIRCLE_SIZE = 0.03 # IN PERCENT
MY_CAR_CIRCLE_MIN_SIZE = 0.024 # IN KILOMETERS
MY_CAR_CIRCLE_MAX_SIZE = 0.3 # IN KILOMETERS

CAR_FORWARD_SIZE = 0.0015 # IN KILOMETERS
CAR_BACKWARD_SIZE = 0.00075 # IN KILOMETERS
CAR_ROTATION_SIZE = 3.6 # IN DEGRESS

CAR_PROBABILITY = 0.0 # IN PERCENTAGE

# BUTTONS
BUTTON_WIDTH = 0.25 # IN PERCENTAGE
BUTTON_HEIGHT = 0.04 # IN PERCENTAGE

PILOT_POS = Vec2(0.2, 0.9)
RECALCULATE_POS = Vec2(0.5, 0.9)
CANCEL_POS = Vec2(0.8, 0.9)

# TEXTURES

BUILDING_1_TEXTURE = Texture2D('textures/polygon/building_1.jpg', 1)
BUILDING_1_TEXTURE = Texture2D('textures/polygon/building_2.jpg', 1)
BUILDING_3_TEXTURE = Texture2D('textures/polygon/building_3.jpg', 1)

WATER_TEXTURE = Texture2D('textures/polygon/water.jpg', 1)
GRASS_TEXTURE = Texture2D('textures/polygon/grass.jpg', 1)

ASPHALT_TEXTURE = Texture2D('textures/line_string/asphalt.jpg', 1)

BUILDING_BRICKS_TEXTURE_PATH = 'textures/polygon/building_1.jpg'
BUILDING_CONCRETE_TEXTURE_PATH = 'textures/polygon/building_2.jpg'
BUILDING_PAINT_TEXTURE_PATH = 'textures/polygon/building_3.jpg'

WATER_TEXTURE_PATH = 'textures/polygon/water.jpg'
GRASS_TEXTURE_PATH = 'textures/polygon/grass.jpg'

ASPHALT_TEXTURE_PATH = 'textures/line_string/asphalt.jpg'
SELECTED_TEXTURE_PATH = 'textures/line_string/selected.jpg'

ORIGIN_TEXTURE_PATH = 'textures/point/origin.png'
DESTINY_TEXTURE_PATH = 'textures/point/destiny.png'

ACCIDENT_TEXTURE_PATH = 'textures/point/accident.png'
CAMERA_TEXTURE_PATH = 'textures/point/camera.png'
POLICE_TEXTURE_PATH = 'textures/point/police.png'
POTHOLE_TEXTURE_PATH = 'textures/point/pothole.png'

WHITE_CAR_TEXTURE_PATH = 'textures/car/white_car.png'
YELLOW_CAR_TEXTURE_PATH = 'textures/car/yellow_car.png'
BLUE_CAR_TEXTURE_PATH = 'textures/car/blue_car.png'
GREEN_CAR_TEXTURE_PATH = 'textures/car/green_car.png'
RED_CAR_TEXTURE_PATH = 'textures/car/red_car.png'
PURPLE_CAR_TEXTURE_PATH = 'textures/car/purple_car.png'

WHITE_CAR_CIRCLE_TEXTURE_PATH = 'textures/car/white_car_circle.png'
YELLOW_CAR_CIRCLE_TEXTURE_PATH = 'textures/car/yellow_car_circle.png'
BLUE_CAR_CIRCLE_TEXTURE_PATH = 'textures/car/blue_car_circle.png'
GREEN_CAR_CIRCLE_TEXTURE_PATH = 'textures/car/green_car_circle.png'
RED_CAR_CIRCLE_TEXTURE_PATH = 'textures/car/red_car_circle.png'
PURPLE_CAR_CIRCLE_TEXTURE_PATH = 'textures/car/purple_car_circle.png'

PILOT_TEXTURE_PATH = 'textures/button/pilot_button.png'
PILOT_HOVER_TEXTURE_PATH = 'textures/button/pilot_hover_button.png'

RECALCULATE_TEXTURE_PATH = 'textures/button/recalculate_button.png'
RECALCULATE_HOVER_TEXTURE_PATH = 'textures/button/recalculate_hover_button.png'

CANCEL_TEXTURE_PATH = 'textures/button/cancel_button.png'
CANCEL_HOVER_TEXTURE_PATH = 'textures/button/cancel_hover_button.png'

# SOUNDS

FORWARD_SOUND_PATH = 'sounds/car/forward.mp3'
LEFT_SOUND_PATH = 'sounds/car/left.mp3'
RIGHT_SOUND_PATH = 'sounds/car/right.mp3'
FINISH_SOUND_PATH = 'sounds/car/finish.mp3'

POTHOLE_SOUND_PATH = 'sounds/point/pothole.mp3'
ACCIDENT_SOUND_PATH = 'sounds/point/accident.mp3'
POLICE_SOUND_PATH = 'sounds/point/police.mp3'
CAMERA_SOUND_PATH = 'sounds/point/camera.mp3'

RECALCULATE_SOUND_PATH = 'sounds/path/recalculate.mp3'
CANCEL_SOUND_PATH = 'sounds/path/cancel.mp3'
PILOT_ENABLE_SOUND_PATH = 'sounds/path/pilot_enable.mp3'
PILOT_DISABLE_SOUND_PATH = 'sounds/path/pilot_disable.mp3'
PILOT_UNAVAILABLE_SOUND_PATH = 'sounds/path/pilot_unavailable.mp3'

MAP_PATH = 'maps/russas.geojson'

# CAMERA
CAMERA_SPEED = 0.25 # IN PERCENTAGE
CAMERA_ANIMATED = False # IN BOOLEAN