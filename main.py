from OpenGL.GL import *
from OpenGL.GLUT import *

from map import Map
from vector import Vector2
from rgb import hexToRGB, hexToRGBA

location = Map('russas.geojson')

LINE_WIDTH = 0.0001

is_dragging = False
last_click_pos = Vector2(0, 0)


def initializeGL():
    glClearColor(*hexToRGBA('#F2EFE9', 1))

    glEnable(GL_POINT_SMOOTH)
    glLineWidth(2)
    glPointSize(5)

def paintGL():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(location.min.x, location.max.x, location.min.y, location.max.y, -1, 1)

    # DRAW POLYGONS
    for polygon in location.polygons:
        if polygon.type == 'water':
            glColor3f(*hexToRGB('#AAD3DF'))
        elif polygon.type == 'wood':
            glColor3f(*hexToRGB('#B8D4A7'))
        else:
            glColor3f(*hexToRGB('#D9D0C9'))
        
        for coord in polygon.coords:
            glBegin(GL_POLYGON)
            
            for point in coord:
                glVertex2f(point.x, point.y)

            glEnd()

    # DRAW POLYGON BORDERS
    glColor3f(*hexToRGB('#C6B9AE'))
    for polygon in location.polygons:
        if polygon.type in ('water', 'wood'):
            continue
        
        for coord in polygon.coords:
            glBegin(GL_LINE_LOOP)

            for point in coord:
                glVertex2f(point.x, point.y)

            glEnd()

    # DRAW LINES
    glColor3f(*hexToRGB('#FFFFFF'))
    for line in location.lines:
        # glBegin(GL_QUADS)

        # for coord, next_coord in zip(line.coords[:-1], line.coords[1:]):
        #     delta = next_coord - coord
        #     normal = Vector2(-delta.y, delta.x).normalize()

        #     p0 = coord + normal * (LINE_WIDTH / 2)
        #     p1 = coord - normal * (LINE_WIDTH / 2)
        #     p2 = next_coord - normal * (LINE_WIDTH / 2)
        #     p3 = next_coord + normal * (LINE_WIDTH / 2)

        #     glVertex2f(p0.x, p0.y)
        #     glVertex2f(p1.x, p1.y)
        #     glVertex2f(p2.x, p2.y)
        #     glVertex2f(p3.x, p3.y)

        # glEnd()

        glBegin(GL_LINES)

        for point, next_point in zip(line.coords[:-1], line.coords[1:]):
            glVertex2f(point.x, point.y)
            glVertex2f(next_point.x, next_point.y)

        glEnd()

    glBegin(GL_POINTS)
    for point in location.points:
        if point.type == 'tree':
            glColor3f(*hexToRGB('#B8D4A7'))
        else:
            glColor3f(*hexToRGB('#FFFFFF'))

        glVertex2f(point.coord.x, point.coord.y)

    glEnd()

    glFlush()


def normalizeXY(coord: Vector2):
    window = Vector2(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    coord = Vector2(coord.x, window.y - coord.y)

    delta = location.max - location.min

    return (coord / window) * delta + location.min


def mouseGL(button, state, x, y):
    if button in (3, 4) and state == GLUT_DOWN:
        norm = normalizeXY(Vector2(x, y))

        scale = 0.1 if button == 3 else -0.1

        location.min += (norm - location.min) * scale
        location.max -= (location.max - norm) * scale

        glutPostRedisplay()

    if button == GLUT_LEFT_BUTTON:
        global last_click_pos, is_dragging

        if state == GLUT_DOWN:
            is_dragging = True
            last_click_pos = normalizeXY(Vector2(x, y))
        else:
            is_dragging = False
            last_click_pos = 0, 0


def motionGL(x, y):
    if is_dragging:
        norm = normalizeXY(Vector2(x, y))

        delta = (norm - last_click_pos) * -1

        location.min += delta
        location.max += delta

        glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow('Mapas')

initializeGL()

glutDisplayFunc(paintGL)
glutMouseFunc(mouseGL)
glutMotionFunc(motionGL)

glutMainLoop()
