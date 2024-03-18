from OpenGL.GL import *
from OpenGL.GLUT import *

from map import Map
from vector import Vector2
from rgb import hexToRGB, hexToRGBA, randomRGB
 
location = Map('russas.geojson')

LINE_WIDTH = 0.0001

is_dragging = False
last_click_pos = Vector2(0, 0)

def initializeGL():
    glClearColor(*hexToRGBA('#2B2D31', 1))
    
    glEnable(GL_POINT_SMOOTH)
    glLineWidth(10)
    glPointSize(3)

def paintGL():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(location.min.x, location.max.x, location.min.y, location.max.y, -1, 1)
    
    for polygon in location.polygons:
        if polygon.type == 'water':
            glColor3f(*hexToRGB('#5C64F4'))
        else:
            glColor3f(*hexToRGB('#232428'))
        
        glBegin(GL_POLYGON)
        
        for coord in polygon.coords:
            glVertex2f(coord.x, coord.y)
            
        glEnd()
    
    glColor3f(*hexToRGB('#131110'))
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
        
        glBegin(GL_LINE_STRIP)
        
        for coord in line.coords:
            glVertex2f(coord.x, coord.y)
        
        glEnd()
     
    glColor3f(*hexToRGB('#EC4444'))
    for line in location.lines:
        glBegin(GL_POINTS)
        
        for coord in line.coords:
            glVertex2f(coord.x, coord.y)
        
        glEnd()
        
    glColor3f(*hexToRGB('#23A559'))
    glBegin(GL_POINTS)
    
    for point in location.points:
        
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