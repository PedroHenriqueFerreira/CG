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

key_down: dict[str, bool] = {}

texture: dict[str, int] = {}

def load_texture(filename: str):
    image = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
    
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
    coord = (Vec2(x, window.y - y) / window) * 2 - 1
    
    return (coord - location.offset) / location.scale

def initGL():
    global texture_grass, texture_water
    
    glClearColor(*BG_COLOR, 1)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    texture['car'] = load_texture('car.png')
    
pos = Vec2(0, 0)
car_width = 0.01

i = Vec2(1, 0)
j = Vec2(0, 1)

def paintGL():   
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    # gluPerspective(55, glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT), 0.01, 1000)

    # glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()
    
    # aa = Mat2(i.x, j.x, i.y, j.y) * Vec2(0, -0.1)
    
    # gluLookAt(pos.x + aa.x, pos.y + aa.y, 0.05, pos.x, pos.y, 0, 0, 0, 1)

    glTranslatef(location.offset.x, location.offset.y, 0)
    glScalef(location.scale, location.scale, 1)

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
    
    # DRAW TEXTS
    glColor3f(*TEXT_COLOR)
    for text in location.texts:
        w = sum(glutBitmapWidth(GLUT_BITMAP_9_BY_15, ord(char)) for char in text.value)
        h = glutBitmapHeight(GLUT_BITMAP_9_BY_15)
        
        width = 2 * w / (glutGet(GLUT_WINDOW_WIDTH) * location.scale)
        height = h / (glutGet(GLUT_WINDOW_HEIGHT) * location.scale)
        
        if text.max_width < width:
            continue
        
        glRasterPos2f(text.coord.x - width / 2, text.coord.y - height / 2)
        
        for char in text.value:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    # DRAW CAR
    glBindTexture(GL_TEXTURE_2D, texture['car'])
    
    glPushMatrix()
    glMultMatrixf([[i.x, i.y, 0, 0], [j.x, j.y, 0, 0], [0, 0, 1, 0], [pos.x, pos.y, 0, 1]])
    
    glBegin(GL_QUADS)
    
    glTexCoord2f(0,0)
    glVertex2f(- car_width, - car_width)
    glTexCoord2f(1,0)
    glVertex2f(+ car_width, - car_width)
    glTexCoord2f(1,1)
    glVertex2f(+ car_width, + car_width)
    glTexCoord2f(0,1)
    glVertex2f(- car_width, + car_width)
    
    glEnd()
    
    glPopMatrix()
    
    glBindTexture(GL_TEXTURE_2D, 0)
    
        
    glutSwapBuffers()

def mouseGL(button: int, state: int, x: int, y: int):
    global mouse_down, mouse_moving
    
    coord = normalize(x, y)
    
    # ZOOM EVENT
    if button in (3, 4) and state == GLUT_DOWN:
        sign = 1 if button == 3 else -1
        
        location.zoom(coord, sign)

    # CLICK EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        if mouse_moving:
            return
        
        location.select(coord)
        
    # DRAG EVENT
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouse_down = coord
        mouse_moving = False

def motionGL(x: int, y: int):
    global mouse_moving
    
    mouse_moving = True
    
    coord = normalize(x, y)
    
    location.move(mouse_down - coord)

def keyboardGL(key: str, x: int, y: int):
    key_down[key] = True

def keyboardUpGL(key: str, x: int, y: int):
    key_down[key] = False

def timerGL(value: int):
    global pos, i, j
    
    glutTimerFunc(1000 // FPS, timerGL, 0)
    
    if key_down.get(b'w'):
        pos += j * SPEED
    
    if key_down.get(b's'):
        pos -= j * SPEED
        
    if key_down.get(b'a'):
        i = Mat2.rotation(ROTATE_SPEED) * i
        j = Mat2.rotation(ROTATE_SPEED) * j
    
    if key_down.get(b'd'):
        i = Mat2.rotation(-ROTATE_SPEED) * i
        j = Mat2.rotation(-ROTATE_SPEED) * j    
        
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
