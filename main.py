from OpenGL.GL import *
from OpenGL.GLUT import *

from map import Map
from vector import Vector2
from rgb import hexToRGB, hexToRGBA

from astar import aStar

location = Map('russas.geojson')

click_pos = Vector2(0, 0)
is_moving = False

path: list[Vector2] | None = None
distance: float = 0

start_pos: Vector2 | None = None
goal_pos: Vector2 | None = None

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
    glBegin(GL_TRIANGLES)
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
    glBegin(GL_QUADS)
    for line in location.lines:
        for quad, next in zip(line.quads, line.quads[1:] + [None]):
            for point in quad:
                glVertex2f(point.x, point.y)
            
            if next is  None:
                continue
            
            for point in [quad[2], quad[3], next[0], next[1]]:
                glVertex2f(point.x, point.y)
    glEnd()
    
    glColor3f(*hexToRGB('#FA0A44'))
    
    # DRAW POINTS
    glBegin(GL_POINTS)
    if start_pos is not None:
        glVertex2f(start_pos.x, start_pos.y)
    if goal_pos is not None:
        glVertex2f(goal_pos.x, goal_pos.y)    
    glEnd()
    
    #DRAW PATH
    if path is not None:
        glBegin(GL_QUADS)
        
        for line in location.lines:
            for i, (prev, curr, quad) in enumerate(zip(line.coords[:-1], line.coords[1:], line.quads)):
                if prev not in path or curr not in path:
                    continue
                
                for point in quad:
                    glVertex2f(point.x, point.y)
            
                if i >= len(line.coords) - 2:
                    continue
                
                next = line.coords[i + 2]
                
                if next not in path:
                    continue
                
                next_quad = line.quads[i + 1]
                
                for point in [quad[2], quad[3], next_quad[0], next_quad[1]]:
                    glVertex2f(point.x, point.y)
            
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
        
        if Vector2.distance(min, max) < text_width:
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
    global click_pos, is_moving, path, distance, start_pos, goal_pos
    
    # ZOOM EVENT
    if button in (3, 4) and state == GLUT_DOWN:
        scale = 0.1 if button == 3 else -0.1
        
        norm = normalizeGL(Vector2(x, y))
    
        location.min += (norm - location.min) * scale
        location.max -= (location.max - norm) * scale
        
        glutPostRedisplay()

    # DRAGGING EVENT
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        click_pos = normalizeGL(Vector2(x, y))
            
        is_moving = False

    # CLICK EVENT
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP and not is_moving:
        norm = normalizeGL(Vector2(x, y))
        
        point = norm.closest(location.graph.keys())
        
        path = None
        distance = 0
        
        if start_pos is None:
            start_pos = point
        elif start_pos == point:
            start_pos = None
        elif goal_pos is None or goal_pos != point:
            goal_pos = point
        elif goal_pos == point:
            goal_pos = None
        
        if start_pos is None and goal_pos is not None:
            start_pos, goal_pos = goal_pos, start_pos
            
        if start_pos is not None and goal_pos is not None:
            path, distance = aStar(location.graph, start_pos, goal_pos)
            
            print(distance)
            
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
