from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from settings import *

from structures.matrix import Mat2
from structures.vector import Vec2
from objects.map import Map

map = None

window = Vec2(WINDOW_WIDTH, WINDOW_HEIGHT)

mouse_down = Vec2(0, 0)
mouse_moving = False

key_down: dict[str, bool] = {}


def normalize(x: int, y: int):
    coord = (Vec2(x, window.y - y) / window) * 2 - 1

    return (coord - map.offset) / map.scale


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

def paintGL():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, window.x / window.y, 0.01, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    camera = Mat2(map.car.i.x, map.car.j.x, map.car.i.y, map.car.j.y) * Vec2(0, -0.05)
    gluLookAt(map.car.pos.x + camera.x, map.car.pos.y + camera.y, 0.05, map.car.pos.x, map.car.pos.y, 0, 0, 0, 1)

    # if len(map.line_strings.get('path', [])) > 0:
    #     gluLookAt(0, 0, 1, 0, 0, 0, map.car.j.x, map.car.j.y, 0)

    #     glScalef(map.scale, map.scale, 1)
    #     glTranslatef(-map.car.pos.x, -map.car.pos.y, 0)
    # else:
    #     # gluLookAt(-map.offset.x, -map.offset.y, 1 / map.scale, -map.offset.x, -map.offset.y, 0, 0, 1, 0)
    #     gluLookAt(0, 0, 1, 0, 0, 0, 0, 1, 0)

    #     glTranslatef(map.offset.x, map.offset.y, 0)
    #     glScalef(map.scale, map.scale, 1)

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
    for type in reversed(POINT_COLOR):
        if type not in map.points:
            continue

        glColor3f(*POINT_COLOR[type])

        for point in map.points[type]:
            point.draw()

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

    coord = normalize(x, y)

    # ZOOM EVENT
    if button in (3, 4) and state == GLUT_DOWN:
        sign = 1 if button == 3 else -1

        map.zoom(coord, sign)

    # DRAG EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouse_down = coord
        mouse_moving = False

    # CLICK EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        if mouse_moving:
            return

        map.select(coord)


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

    near = map.car.pos.nearest(map.graph.keys())
    
    distance = Vec2.distance(map.car.pos, near)
    
    if key_down.get(b'w'):
        if distance != 0 and distance < CAR_FORWARD_SPEED:
            map.car.pos = near
        
        elif map.car.pos in map.graph:
            degrees = []
            
            for node in map.graph[map.car.pos]:
                degrees.append(Vec2.degrees(map.car.j, node - map.car.pos))
            
            map.car.rotate(min(degrees, key=lambda x: abs(x)))
            
            map.car.move(CAR_FORWARD_SPEED + 0.00000001)
        else:
            map.car.move(CAR_FORWARD_SPEED)

    if key_down.get(b's'):
        if distance != 0 and distance < CAR_BACKWARD_SPEED:
            map.car.pos = near
        
        elif map.car.pos in map.graph:
            degrees = []
            
            for node in map.graph[map.car.pos]:
                degrees.append(Vec2.degrees(-1 * map.car.j, node - map.car.pos))
            
            map.car.rotate(min(degrees, key=lambda x: abs(x)))
            
            map.car.move(-CAR_BACKWARD_SPEED - 0.00000001)
        else:
            map.car.move(-CAR_BACKWARD_SPEED)

    if key_down.get(b'a'):
        if map.car.pos in map.graph:
            map.car.rotate_left()
        
    if key_down.get(b'd'):
        if map.car.pos in map.graph:
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
glutMotionFunc(motionGL)
glutKeyboardFunc(keyboardGL)
glutKeyboardUpFunc(keyboardUpGL)
glutReshapeFunc(reshapeGL)

glutTimerFunc(1000 // FPS, timerGL, 0)

glutMainLoop()
