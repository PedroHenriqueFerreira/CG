from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image

from settings import *

from vec import Vec2, Mat2
from map import Map

location = Map('russas.geojson')

mouse_down = Vec2(0, 0)
mouse_moving = False

w_down = False
a_down = False
s_down = False
d_down = False

def loadTexture(filename: str):
    image = Image.open(filename)
    
    data = image.tobytes()
    
    width, height = image.size
    
    texture_id = glGenTextures(1)
    
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    glBindTexture(GL_TEXTURE_2D, 0)
    
    return texture_id

def normalize(x: int, y: int):
    window = Vec2(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    coord = Vec2(x, window.y - y)

    return (coord / window) * (location.max - location.min) + location.min

def initGL():
    global texture_grass, texture_water
    
    glClearColor(*BG_COLOR, 1)
    
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
pos = (location.max + location.min) / 2
car_width = 0.00005
car_height = 0.0001

i = Vec2(1, 0)
j = Vec2(0, 1)

def paintGL():   
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(location.min.x, location.max.x, location.min.y, location.max.y, -1, 1)

    # glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()

    glBegin(GL_TRIANGLES)
    
    # DRAW POLYGONS
    for type in location.polygons:
        glColor3f(*POLYGON_COLOR[type])
        
        for polygon in location.polygons[type]:
            for point in polygon.triangles:
                glVertex2f(point.x, point.y)
                

    # DRAW LINE STRINGS
    glColor3f(*LINE_STRING_COLOR)
    for line_string in location.line_strings:
        for point in line_string.triangles:
            glVertex2f(point.x, point.y)    
    
    glColor3f(*PATH_COLOR)
    
    # DRAW PATH
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
    
    glPushMatrix()
    
    glMultMatrixf([
        [i.x, i.y, 0, 0],
        [j.x, j.y, 0, 0],
        [0, 0, 1, 0],
        [pos.x, pos.y, 0, 1],
    ])
    
    glBegin(GL_TRIANGLES)
    
    glVertex2f(- car_width, - car_height)
    glVertex2f(+ car_width, - car_height)
    glVertex2f(+ car_width, + car_height)

    glVertex2f(- car_width, - car_height)
    glVertex2f(- car_width, + car_height)
    glVertex2f(+ car_width, + car_height)
    
    glEnd()
    
    glPopMatrix()
    
    
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
    
    glutSwapBuffers()

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

def keyboardGL(key: str, x: int, y: int):
    global w_down, a_down, s_down, d_down
    
    if key == b'w':
        w_down = True
    elif key == b'a':
        a_down = True
    elif key == b's':
        s_down = True
    elif key == b'd':
        d_down = True

def keyboardUpGL(key: str, x: int, y: int):
    global w_down, a_down, s_down, d_down
    
    if key == b'w':
        w_down = False
    elif key == b'a':
        a_down = False
    elif key == b's':
        s_down = False
    elif key == b'd':
        d_down = False

def timerGL(value: int):
    global pos, i, j
    
    glutTimerFunc(1000 // FPS, timerGL, 0)
    
    if w_down:
        pos += j * SPEED
    
    if s_down:
        pos -= j * SPEED
        
    if a_down:
        i = Mat2.rotation_z(ROTATE_SPEED) * i
        j = Mat2.rotation_z(ROTATE_SPEED) * j
    
    if d_down:
        i = Mat2.rotation_z(-ROTATE_SPEED) * i
        j = Mat2.rotation_z(-ROTATE_SPEED) * j    
        
    glutPostRedisplay()
        
glutInit()
glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow('Waze')

initGL()

glutDisplayFunc(paintGL)
glutMouseFunc(mouseGL)
glutMotionFunc(motionGL)

glutKeyboardFunc(keyboardGL)
glutKeyboardUpFunc(keyboardUpGL)

glutTimerFunc(1000 // FPS, timerGL, 0)

glutMainLoop()
