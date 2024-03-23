from OpenGL.GL import *
from OpenGL.GLUT import *

from map import Map
from vector import Vector2
from rgb import hexToRGB, hexToRGBA

location = Map('russas.geojson')

is_dragging = False
last_click_pos = Vector2(0, 0)

def initializeGL():
    glClearColor(*hexToRGBA('#F8F7F7', 1))

    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glLineWidth(2)
    glPointSize(5)

def textGL(coord: Vector2, text: str):
    text_width = 0
    
    for char in text:
        text_width += glutBitmapWidth(GLUT_BITMAP_8_BY_13, ord(char))
    
    window_width = glutGet(GLUT_WINDOW_WIDTH)
    
    x = coord.x - (text_width / window_width) * (location.max.x - location.min.x) / 2
    y = coord.y
    
    glRasterPos2f(x, y)

    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(char))

def paintGL():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(location.min.x, location.max.x, location.min.y, location.max.y, -1, 1)

    # DRAW POLYGONS
    for polygon in location.polygons:
        if polygon.type == 'grass':
            glColor3f(*hexToRGB('#D3F8E2'))
        elif polygon.type == 'water':
            glColor3f(*hexToRGB('#90DAEE'))
        else:
            glColor3f(*hexToRGB('#E8E9ED'))
                    
        for coord in polygon.triangles:
            glBegin(GL_TRIANGLES)
            
            for point in coord:
                glVertex2f(point.x, point.y)

            glEnd()

    # DRAW BUILDING BORDERS
    glColor3f(*hexToRGB('#D9DBE7'))
    for polygon in location.polygons:
        if polygon.type != 'building':
            continue
        
        for coord in polygon.coords:
            glBegin(GL_LINE_LOOP)
            
            for point in coord:
                glVertex2f(point.x, point.y)

            glEnd()

    # DRAW LINES
    glColor3f(*hexToRGB('#B1BFCD'))
    for line in location.lines:
        glBegin(GL_QUADS)

        for point in line.quads:
            glVertex2f(point.x, point.y)

        glEnd()
     
    # DRAW POLYGONS NAMES
    glColor3f(*hexToRGB('#7D7D7D'))
    for polygon in location.polygons:
        if polygon.name is None:
            continue
        
        textGL(polygon.centroid(), polygon.name)
        
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
