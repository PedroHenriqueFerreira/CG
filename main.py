from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from settings import *

from structures.vector import Vec2
from objects.map import Map
from objects.texture import Texture
from objects.camera import Camera

map = None

window = Vec2(WINDOW_WIDTH, WINDOW_HEIGHT)

mouse_down = Vec2(0, 0)
mouse_moving = False

key_down: dict[str, bool] = {}

texture: dict[str, Texture] = {}

def normalize(x: int, y: int):
    coord = (Vec2(x, window.y - y) / window) * 2 - 1
    aspect_ratio = Vec2(window.x / window.y, 1)

    return (coord * aspect_ratio / map.scale) + map.offset

def initializeGL():
    global map

    glClearColor(*BG_COLOR, 1)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glPointSize(6)
    glLineWidth(2)

    map = Map(MAP_PATH)
    
    for type in POINT_TEXTURE:
        texture[type] = Texture(POINT_TEXTURE[type])

sign = -1
pulse = 1

cam = Camera()

def paintGL():
    global pulse, sign
    
    if pulse >= 1.25 or pulse <= 1:
        sign *= -1
    
    pulse += sign * 0.02
    
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, window.x / window.y, 0.001, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if len(map.line_strings.get('path', [])) > 0:
        camera = map.car.pos - map.car.j * 0.025

        cam.update([
            camera.x, camera.y, 1 / map.scale, 
            map.car.pos.x, map.car.pos.y, 0, 
            map.car.j.x, map.car.j.y, 0
        ])

        gluLookAt(*cam.values)
        
    else:
        cam.update([
            map.offset.x, map.offset.y, 1 / map.scale, 
            map.offset.x, map.offset.y, 0, 
            0, 1, 0
        ])
        
        gluLookAt(*cam.values)

    # DRAW POLYGONS
    for type in reversed(POLYGON_COLOR):
        if type not in map.polygons:
            continue

        glColor3f(*POLYGON_COLOR[type])

        for polygon in map.polygons[type]:
            polygon.draw()

    # DRAW LINE STRINGS
    for type in reversed(LINE_STRING_COLOR):
        if type not in map.line_strings:
            continue

        glColor3f(*LINE_STRING_COLOR[type])

        for line_string in map.line_strings[type]:
            line_string.draw()
    
    # DRAW POINTS
    for type in reversed(POINT_TEXTURE):
        if type not in map.points:
            continue

        for point in map.points[type]:
            point.draw(map.car.rotation, 1, texture[type].id)

    # DRAW POLYGON NAMES
    glColor3f(*TEXT_COLOR)
    for type in map.polygons:
        for polygon in map.polygons[type]:
            text_size = 2 * polygon.name_size / (window * map.scale)

            if polygon.width < text_size.x:
                continue

            glRasterPos2f(polygon.center.x - text_size.x / 2,
                          polygon.center.y - text_size.y / 2)

            for char in polygon.name:
                glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    # DRAW CAR
    map.car.draw()

    glutSwapBuffers()

def mouseGL(button: int, state: int, x: int, y: int):
    global mouse_down, mouse_moving
    
    if button != GLUT_LEFT_BUTTON:
        return
    
    coord = normalize(x, y)

    # DRAG EVENT
    if state == GLUT_DOWN:
        mouse_down = coord
        mouse_moving = False

    # CLICK EVENT
    else:
        if mouse_moving:
            return

        map.select(coord)

def mouseWheelGL(button: int, direction: int, x: int, y: int):
    coord = normalize(x, y)
    
    map.zoom(coord, direction)

def motionGL(x: int, y: int):
    global mouse_moving

    mouse_moving = True

    coord = normalize(x, y)

    map.move(mouse_down - coord)

def keyboardGL(key: str, x: int, y: int):
    key_down[key] = True

def keyboardUpGL(key: str, x: int, y: int):
    key_down[key] = False

def reshapeGL(width: int, height: int):
    window.x, window.y = width, height

    glViewport(0, 0, width, height)

def timerGL(value: int):
    global pos, i, j

    glutTimerFunc(1000 // FPS, timerGL, 0)

    nearest = map.car.pos.nearest(map.graph.keys())
    distance = Vec2.distance(map.car.pos, nearest)
    
    if key_down.get(b'w'):
        if distance < CAR_FORWARD_SPEED - 1e-8:
            map.car.pos = nearest
            
            rotation = float('inf')
            
            for neighbor in map.graph[nearest]:
                degree = Vec2.degrees(map.car.j, neighbor - nearest)
                
                if abs(rotation) > abs(degree):
                    rotation = degree
            
            map.car.rotate(rotation)

        map.car.move(CAR_FORWARD_SPEED)

    if key_down.get(b's'):
        if distance < CAR_BACKWARD_SPEED - 1e-8:
            map.car.pos = nearest
            
            rotation = float('inf')
            
            for neighbor in map.graph[nearest]:
                degree = Vec2.degrees(map.car.j * -1, neighbor - nearest)
                
                if abs(rotation) > abs(degree):
                    rotation = degree
            
            map.car.rotate(rotation)

        map.car.move(-CAR_BACKWARD_SPEED)

    if key_down.get(b'a'):
        if distance < CAR_WIDTH:
            map.car.pos = nearest
            
            map.car.rotate_left()
        
    if key_down.get(b'd'):
        if distance < CAR_WIDTH:
            map.car.pos = nearest
            
            map.car.rotate_right()   

    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow('Waze')

initializeGL()

glutDisplayFunc(paintGL)
glutMouseFunc(mouseGL)
glutMouseWheelFunc(mouseWheelGL)
glutMotionFunc(motionGL)
glutKeyboardFunc(keyboardGL)
glutKeyboardUpFunc(keyboardUpGL)
glutReshapeFunc(reshapeGL)

glutTimerFunc(1000 // FPS, timerGL, 0)

glutMainLoop()
