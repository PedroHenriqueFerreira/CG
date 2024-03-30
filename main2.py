from OpenGL.GL import *
from OpenGL.GLUT import *

from map2 import Map
from vec import Vec2
from rgb import hexToRGB, hexToRGBA

from settings import ZOOM_FACTOR

location = Map('russas.geojson')

min, max = location.min, location.max

click_pos = Vec2(0, 0)
is_moving = False

angle = 0

def initializeGL():
    glClearColor(*hexToRGBA('#F8F7F7', 1))

    glEnable(GL_POINT_SMOOTH)
    
    glLineWidth(2)
    glPointSize(8)


def textWidthGL(text: str):
    text_width = 0

    for char in text:
        text_width += glutBitmapWidth(GLUT_BITMAP_8_BY_13, ord(char))

    window_width = glutGet(GLUT_WINDOW_WIDTH)

    return (text_width / window_width) * (max.x - min.x)

def paintGL():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(min.x, max.x, min.y, max.y, -1, 1)

    # glTranslatef((location.max.x + location.min.x) / 2, (location.max.y + location.min.y) / 2, 0)
    # glRotatef(angle, 0, 0, 1)
    # glTranslatef(- (location.max.x + location.min.x) / 2, - (location.max.y + location.min.y) / 2, 0)

    # DRAW LINES
    glColor3f(*hexToRGB('#B1BFCD'))
    glBegin(GL_TRIANGLES)
    for line in location.line_strings:   
        for coord in line.coords:
            for point in coord:
                glVertex2f(point.x, point.y)
    glEnd()

    glFlush()

def normalizeGL(coord: Vec2):
    window = Vec2(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    coord = Vec2(coord.x, window.y - coord.y)

    delta = max - min

    return (coord / window) * delta + min

def mouseGL(button: int, state: int, x: int, y: int):
    global click_pos, is_moving, min, max

    # ZOOM EVENT
    if button in (3, 4) and state == GLUT_DOWN:
        scale = ZOOM_FACTOR if button == 3 else -ZOOM_FACTOR

        norm = normalizeGL(Vec2(x, y))

        min_ = min + (norm - min) * scale
        max_ = max - (max - norm) * scale

        if min_.x < location.min.x or min_.y < location.min.y:
            return
        
        if max_.x > location.max.x or max_.y > location.max.y:
            return

        min, max = min_, max_
            
        glutPostRedisplay()

    # DRAGGING EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        click_pos = normalizeGL(Vec2(x, y))
        is_moving = False

    # CLICK EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP and not is_moving:
        ...

        glutPostRedisplay()

def motionGL(x: int, y: int):
    global is_moving, min, max

    is_moving = True

    norm = normalizeGL(Vec2(x, y))

    delta = (norm - click_pos) * -1

    min_ = min + delta
    max_ = max + delta

    if min_.x < location.min.x or min_.y < location.min.y:
        return
    
    if max_.x > location.max.x or max_.y > location.max.y:
        return
    
    min, max = min_, max_
    
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow('WAZE')

initializeGL()

glutDisplayFunc(paintGL)
glutMouseFunc(mouseGL)
glutMotionFunc(motionGL)

glutMainLoop()
