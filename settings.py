import glm

from glm import vec3

from structures.vector import Vec2, Vec3

# GENERAL
BG_COLOR = Vec3.from_hex('#555A60')

WINDOW_WIDTH = 800 # IN PIXELS
WINDOW_HEIGHT = 800 # IN PIXELS

FPS = 60 # IN INTEGER

ZOOM_FACTOR = 1.1 # IN PERCENTAGE

CIRCLE_SEGMENTS = 30 # IN INTEGER

# LINE STRINGS 
LINE_STRING_SIZE = 0.006 # IN KILOMETERS
LINE_STRING_COLOR = Vec3.from_hex('#363D44')

LINE_STRING_TEXT_THICKNESS = 2 # IN INTEGER
LINE_STRING_TEXT_SIZE = 0.015 # IN PERCENTAGE
LINE_STRING_TEXT_MIN_SIZE = 0.002 # IN KILOMETERS
LINE_STRING_TEXT_MAX_SIZE = 0.012 # IN KILOMETERS
LINE_STRING_TEXT_COLOR = Vec3.from_hex('#AAAAAA')

PATH_SIZE = 0.006 # IN KILOMETERS
# PATH_COLOR = Color.hex('#04E5FE')
PATH_COLOR = Vec3.from_hex('#FFFFFF')

# POLYGONS
POLYGON_TEXT_THICKNESS = 2 # IN INTEGER
POLYGON_TEXT_SIZE = 0.018 # IN PERCENTAGE
POLYGON_TEXT_MIN_SIZE = 0.0024 # IN KILOMETERS
POLYGON_TEXT_MAX_SIZE = 0.015 # IN KILOMETERS
POLYGON_TEXT_COLOR = Vec3.from_hex('#AAAAAA')

# GRASS_COLOR = Color.hex('#527C6D')
# WATER_COLOR = Color.hex('#516C7D')
# BUILDING_COLOR = Color.hex('#464B51')
# UNKNOWN_COLOR = Color.hex('#51565C')

GRASS_COLOR = Vec3.from_hex('#FFFFFF')
WATER_COLOR = Vec3.from_hex('#FFFFFF')
BUILDING_COLOR = Vec3.from_hex('#FFFFFF')
UNKNOWN_COLOR = Vec3.from_hex('#FFFFFF')


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

BUILDING_BRICKS_TEXTURE_PATH = 'textures/polygon/building_1.jpg'
BUILDING_CONCRETE_TEXTURE_PATH = 'textures/polygon/building_2.jpg'
BUILDING_PAINT_TEXTURE_PATH = 'textures/polygon/building_3.jpg'

WATER_TEXTURE_PATH = 'textures/polygon/water.jpg'
GRASS_TEXTURE_PATH = 'textures/polygon/grass.jpg'

ASPHALT_TEXTURE_PATH = 'textures/line_string/asphalt.jpg'
PATH_TEXTURE_PATH = 'textures/line_string/path.jpg'

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

#### SETTINGS REFACTORING


# TEXTURES

BUILDING_DIFFUSE_TEXTURE_FILE = 'textures/polygon/building_diffuse.jpg'
BUILDING_NORMAL_TEXTURE_FILE = 'textures/polygon/building_normal.jpg'

WATER_DIFFUSE_TEXTURE_FILE = 'textures/polygon/water_diffuse.jpg'
WATER_NORMAL_TEXTURE_FILE = 'textures/polygon/water_normal.jpg'

GRASS_DIFFUSE_TEXTURE_FILE = 'textures/polygon/grass_diffuse.jpg'
GRASS_NORMAL_TEXTURE_FILE = 'textures/polygon/grass_normal.jpg'

UNKNOWN_DIFFUSE_TEXTURE_FILE = 'textures/polygon/unknown_diffuse.jpg'
UNKNOWN_NORMAL_TEXTURE_FILE = 'textures/polygon/unknown_normal.jpg'

ROAD_DIFFUSE_TEXTURE_FILE = 'textures/line_string/road_diffuse.jpg'
ROAD_NORMAL_TEXTURE_FILE = 'textures/line_string/road_normal.jpg'

PATH_DIFFUSE_TEXTURE_FILE = 'textures/line_string/path_diffuse.jpg'
PATH_NORMAL_TEXTURE_FILE = 'textures/line_string/path_normal.jpg'

GROUND_DIFFUSE_TEXTURE_FILE = 'textures/ground/ground_diffuse.jpg'
GROUND_NORMAL_TEXTURE_FILE = 'textures/ground/ground_normal.jpg'

SKYBOX_TEXTURE_FILES = [
    'textures/skybox/right.png',
    'textures/skybox/left.png',
    'textures/skybox/front.png',
    'textures/skybox/back.png',
    'textures/skybox/top.png',
    'textures/skybox/bottom.png',
]

# SHADERS

DEFAULT_SHADER_VERT_FILE = 'shaders/default.vert'
DEFAULT_SHADER_FRAG_FILE = 'shaders/default.frag'

SKYBOX_SHADER_VERT_FILE = 'shaders/skybox.vert'
SKYBOX_SHADER_FRAG_FILE = 'shaders/skybox.frag'

# MATERIALS

GRASS_AMBIENT_MATERIAL = vec3(1, 1, 1)
GRASS_DIFFUSE_MATERIAL = vec3(1, 1, 1)
GRASS_SPECULAR_MATERIAL = vec3(1, 1, 1)
GRASS_SHININESS_MATERIAL = 32.0

WATER_AMBIENT_MATERIAL = vec3(1, 1, 1)
WATER_DIFFUSE_MATERIAL = vec3(1, 1, 1)
WATER_SPECULAR_MATERIAL = vec3(1, 1, 1)
WATER_SHININESS_MATERIAL = 32.0

BUILDING_AMBIENT_MATERIAL = vec3(1, 1, 1)
BUILDING_DIFFUSE_MATERIAL = vec3(1, 1, 1)
BUILDING_SPECULAR_MATERIAL = vec3(1, 1, 1)
BUILDING_SHININESS_MATERIAL = 32.0

UNKNOWN_AMBIENT_MATERIAL = vec3(1, 1, 1)
UNKNOWN_DIFFUSE_MATERIAL = vec3(1, 1, 1)
UNKNOWN_SPECULAR_MATERIAL = vec3(1, 1, 1)
UNKNOWN_SHININESS_MATERIAL = 32.0

ROAD_AMBIENT_MATERIAL = vec3(1, 1, 1)
ROAD_DIFFUSE_MATERIAL = vec3(1, 1, 1)
ROAD_SPECULAR_MATERIAL = vec3(1, 1, 1)
ROAD_SHININESS_MATERIAL = 32.0

PATH_AMBIENT_MATERIAL = vec3(0.1, 0.1, 0.1)
PATH_DIFFUSE_MATERIAL = vec3(0.5, 0.5, 0.5)
PATH_SPECULAR_MATERIAL = vec3(1.0, 1.0, 1.0)
PATH_SHININESS_MATERIAL = 32.0

GROUND_AMBIENT_MATERIAL = vec3(0.1, 0.1, 0.1)
GROUND_DIFFUSE_MATERIAL = vec3(0.5, 0.5, 0.5)
GROUND_SPECULAR_MATERIAL = vec3(1.0, 1.0, 1.0)
GROUND_SHININESS_MATERIAL = 32.0

# SIZES

ROAD_SIZE = 6 # METERS
PATH_SIZE = 6 # METERS

###