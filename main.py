from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from settings import *

from vec import Vec2
from map import Map

location = Map('russas.geojson')

mouse_down = Vec2(0, 0)
mouse_moving = False

def normalize(x: int, y: int):
    window = Vec2(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    coord = Vec2(x, window.y - y)

    return (coord / window) * (location.max - location.min) + location.min

def initGL():
    glClearColor(*BG_COLOR, 1)

def paintGL():   
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(location.min.x, location.max.x, location.min.y, location.max.y, -1, 1)

    glBegin(GL_TRIANGLES)
    
    # DRAW POLYGONS
    for type in location.polygons:
        for polygon in location.polygons[type]:        
            glColor3f(*POLYGON_COLOR[type])
            for point in polygon.triangles:
                glVertex2f(point.x, point.y)

    # DRAW LINE STRINGS
    glColor3f(*LINE_STRING_COLOR)
    for line_string in location.line_strings:
        for point in line_string.triangles:
            glVertex2f(point.x, point.y)    
    
    # DRAW PATH
    glColor3f(*PATH_COLOR)
    if location.path is not None:
        for point in location.path.triangles:
            glVertex2f(point.x, point.y)
    
    # DRAW START
    if location.start is not None:
        for point in location.start.triangles:
            glVertex2f(point.x, point.y)
    
    # DRAW GOAL
    if location.goal is not None:
        for point in location.goal.triangles:
            glVertex2f(point.x, point.y)
    
    glEnd()
    
    glColor3f(*TEXT_COLOR)
    for type in location.polygons:
        for polygon in location.polygons[type]:
            if polygon.name is None:
                continue
            
            w = sum(glutBitmapWidth(GLUT_BITMAP_9_BY_15, ord(char)) for char in polygon.name)
            width = (w / glutGet(GLUT_WINDOW_WIDTH)) * (location.max.x - location.min.x)

            if Vec2.distance(polygon.min, polygon.max) < width:
                continue

            glRasterPos2f(polygon.center.x - width / 2, polygon.center.y)

            for char in polygon.name:
                glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))
    
    glFlush()

def mouseGL(button: int, state: int, x: int, y: int):
    global mouse_down, mouse_moving
    
    coord = normalize(x, y)
    
    # ZOOM EVENT
    if button in (3, 4) and state == GLUT_DOWN:
        sign = 1 if button == 3 else -1
        
        location.zoom(coord, sign)
            
        glutPostRedisplay()

    # CLICK EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        if mouse_moving:
            return
        
        location.select(coord)

        glutPostRedisplay()
        
    # DRAG EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouse_down = coord
        mouse_moving = False

def motionGL(x: int, y: int):
    coord = normalize(x, y)
    
    global mouse_moving
    mouse_moving = True
    
    location.move(coord - mouse_down)

    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow('WAZE')

initGL()

glutDisplayFunc(paintGL)
glutMouseFunc(mouseGL)
glutMotionFunc(motionGL)

glutMainLoop()
