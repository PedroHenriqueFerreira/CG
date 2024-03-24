from OpenGL.GL import *
from OpenGL.GLUT import *

from map import Map
from vector import Vector2
from rgb import hexToRGB, hexToRGBA, randomRGB

location = Map('russas.geojson')

click_pos = Vector2(0, 0)
is_moving = False

initial = None
final = None

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
    
    return (text_width / window_width) * (location.max.x - location.min.x)

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
        elif polygon.type == 'sand':
            glColor3f(*hexToRGB('#F7ECCF'))
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
     
    # DRAW POINTS
    glBegin(GL_POINTS)
    if initial is not None:
        glColor3f(*hexToRGB('#FF0000'))
        glVertex2f(initial.x, initial.y)
        
    if final is not None:
        glColor3f(*hexToRGB('#00FF00'))
        glVertex2f(final.x, final.y)

    glEnd()
     
    # DRAW POLYGONS NAMES
    glColor3f(*hexToRGB('#7D7D7D'))
    for polygon in location.polygons:
        if polygon.name is None:
            continue
    
        min = polygon.min
        max = polygon.max
        centroid = polygon.centroid
        
        text_width = textWidthGL(polygon.name)
        
        if (max - min).module() < text_width:
            continue
        
        glRasterPos2f(centroid.x - text_width / 2, centroid.y)

        for char in polygon.name:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(char))
        
    glFlush()

def normalizeGL(coord: Vector2):
    window = Vector2(glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    coord = Vector2(coord.x, window.y - coord.y)

    delta = location.max - location.min

    return (coord / window) * delta + location.min

def mouseGL(button: int, state: int, x: int, y: int):
    global click_pos, is_moving, initial, final
    
    # ZOOM EVENT
    if button in (3, 4) and state == GLUT_DOWN:
        scale = 0.1 if button == 3 else -0.1
        
        norm = normalizeGL(Vector2(x, y))
    
        location.min += (norm - location.min) * scale
        location.max -= (location.max - norm) * scale
        
        glutPostRedisplay()

    if button == GLUT_LEFT_BUTTON:
        # DRAGGING EVENT
        if state == GLUT_DOWN:
            click_pos = normalizeGL(Vector2(x, y))
            
            is_moving = False
            
        # CLICK EVENT
        elif is_moving is False:
            norm = normalizeGL(Vector2(x, y))
            
            if initial is None:
                initial = norm.closest([point for line in location.lines for point in line.coords])
            else:
                final = norm.closest([point for line in location.lines for point in line.coords])
                
            glutPostRedisplay()
        
def motionGL(x: int, y: int):
    global is_moving

    is_moving = True
    
    norm = normalizeGL(Vector2(x, y))

    delta = (norm - click_pos) * -1

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
