from OpenGL.GL import *
from OpenGL.GLUT import *

from map2 import Map, LineString
from vec import Vec2

from settings import *

location = Map('russas.geojson')

min, max = location.min, location.max

click_pos = Vec2(0, 0)
is_moving = False

def initializeGL():
    glClearColor(*BG_COLOR)

    glEnable(GL_POINT_SMOOTH)
    glLineWidth(2)
    glPointSize(8)

def paintGL():    
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(min.x, max.x, min.y, max.y, -1, 1)

    # glTranslatef((max.x + min.x) / 2, (max.y + min.y) / 2, 0)
    # glRotatef(angle, 0, 0, 1)
    # glTranslatef(-(max.x + min.x) / 2, -(max.y + min.y) / 2, 0)
    
    # DRAW POLYGONS
    glBegin(GL_TRIANGLES)
    for type in location.polygons:
        for polygon in location.polygons[type]:        
            # MAIN
            glColor3f(*POLYGON_COLOR[type])
            for point in polygon.triangles[0]:
                glVertex2f(point.x, point.y)
                
            # HOLES
            glColor3f(*POLYGON_COLOR['other'])
            for triangle in polygon.triangles[1:]:
                for point in triangle:
                    glVertex2f(point.x, point.y)     
                
    glEnd()
                
    glBegin(GL_TRIANGLES)
    
    # DRAW LINES
    glColor3f(*LINE_COLOR)
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
    
    glFlush()

def normalizeGL(coord: Vec2):
    window = Vec2(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    coord = Vec2(coord.x, window.y - coord.y)

    delta = max - min

    return (coord / window) * delta + min

def mouseGL(button: int, state: int, x: int, y: int):
    # ZOOM EVENT
    if button in (3, 4) and state == GLUT_DOWN:
        global min, max
        
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
        global click_pos, is_moving
        
        click_pos = normalizeGL(Vec2(x, y))
        is_moving = False

    # CLICK EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP and not is_moving:
        location.select(normalizeGL(Vec2(x, y)))

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
