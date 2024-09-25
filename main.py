from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from settings import *

from objects.skybox import SkyBox

from objects.obj import OBJ

from structures.vector import Vec2, Vec3
from objects.map import Map

from objects.textures import Texture2D

map = None

window_width = WINDOW_WIDTH
window_height = WINDOW_HEIGHT

mouse_left_down: Vec2 | None = None
mouse_right_down: Vec2 | None = None

mouse_moving = False

key_down: dict[str, bool] = {}

def window_to_screen(window: Vec2):
    normalized = Vec2(window.x, window_height - window.y) / Vec2(window_width, window_height)
    normalized = normalized * 2 - 1
    
    normalized.x *= window_width / window_height

    return normalized

def screen_to_world(screen: Vec2):
    return screen / map.scale + map.offset

def window_to_world(window: Vec2):
    return screen_to_world(window_to_screen(window))

def initializeGL():
    global map
    
    glClearColor(BG_COLOR.x, BG_COLOR.y, BG_COLOR.z, 1)
    
    glEnable(GL_TEXTURE_2D)
    
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_BLEND)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    glShadeModel(GL_SMOOTH) 
    
    glDepthFunc(GL_LEQUAL)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glPointSize(6)
    
    map = Map(MAP_PATH)

import glm

def paintGL():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(90, window_width / window_height, 0.00001, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if map.my_car:
        eye = map.my_car.pos - map.my_car.j * 0.01

        map.offset = eye
        
        map.view.update(
            glm.vec3(eye.x + map.rotation.x, eye.y + map.rotation.y, 1 / map.scale),
            glm.vec3(map.my_car.pos.x, map.my_car.pos.y, 0),
            glm.vec3(map.my_car.j.x, map.my_car.j.y, 0)
        )

    else:
        map.view.update(
            glm.vec3(map.offset.x, map.offset.y, 1 / map.scale),
            glm.vec3(map.offset.x + map.rotation.x, map.offset.y + map.rotation.y, 0),
            glm.vec3(0, 1, 0)
        )
    
    map.skybox.draw()
    map.ground.draw()
    map.line_strings.draw()
    map.polygons.draw()

    # DRAW POLYGONS
    # map.polygons[0].draw()
    # for polygon in map.polygons:
    #     polygon.draw()

    # DRAW LINE_STRINGS
    # for line_string in map.line_strings:
    #     line_string.draw()

    # if map.path:
    #     map.path.draw()

    # DRAW TEXTS
    # for text in map.texts:
    #     text.draw()

    # DRAW CARS
    # for car in map.cars:
        # car.draw()

    # if map.my_car:
    #     map.my_car.draw()

    # DRAW POINTS
    # for point in map.points:
    #     point.draw()

    # if map.origin:
    #     map.origin.draw()

    # if map.destiny:
    #     map.destiny.draw()

    # DRAW BUTTONS
    # for button in map.buttons:
    #     button.draw()

    glutSwapBuffers()

def mouseGL(button: int, state: int, x: int, y: int):
    global mouse_left_down, mouse_right_down, mouse_moving

    pos = window_to_world(Vec2(x, y))
    
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            mouse_right_down = pos
            mouse_moving = False
            
        else:
            mouse_right_down = None

            map.rotate(Vec2(0, 0))

    else: 
        # DRAG EVENT
        if state == GLUT_DOWN:
            mouse_left_down = pos
            mouse_moving = False

        # CLICK EVENT
        else:
            mouse_left_down = None
            
            if mouse_moving:
                return

            for button in map.buttons:
                if button.hovered:
                    button.click()
                    
                    return
                    
            if map.my_car:
                return

            map.select(pos)

def mouseWheelGL(button: int, direction: int, x: int, y: int):
    pos = window_to_world(Vec2(x, y))

    map.zoom(pos, direction)

def motionGL(x: int, y: int):
    global mouse_moving

    if mouse_left_down:
        mouse_moving = True

        pos = window_to_world(Vec2(x, y))

        map.move(mouse_left_down - pos)
    elif mouse_right_down:
        mouse_moving = True
        
        pos = window_to_world(Vec2(x, y))
        
        map.rotate(mouse_right_down - pos)

def passiveMotionGL(x: int, y: int):
    pos = window_to_screen(Vec2(x, y))
    
    map.hover(pos)
    
def keyboardGL(key: str, x: int, y: int):
    key_down[key] = True

def keyboardUpGL(key: str, x: int, y: int):
    key_down[key] = False

def reshapeGL(width: int, height: int):
    global window_width, window_height
    
    window_width, window_height = width, height

    map.projection.update(window_width / window_height)

    glViewport(0, 0, width, height)

def timerGL(value: int):
    global pos, i, j

    glutTimerFunc(1000 // FPS, timerGL, 0)

    global prev, next

    if map.my_car:
        
        if map.my_car.pilot:
            map.my_car.auto()
        else:
            if key_down.get(b'w'):
                map.my_car.move_forward()
                
            if key_down.get(b's'):
                map.my_car.move_backward()
                
            if key_down.get(b'a'):
                map.my_car.rotate_left()
                
            if key_down.get(b'd'):
                map.my_car.rotate_right()
    
    for car in map.cars:
        car.auto()
    
    glutPostRedisplay()

def joystickGL(button_mask: int, x: int, y: int, z: int):
    # print(button_mask, x, y, z)
    ...

glutInit()
glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow('Waze')

initializeGL()

glutDisplayFunc(paintGL)
glutMouseFunc(mouseGL)
glutMouseWheelFunc(mouseWheelGL)
glutMotionFunc(motionGL)
glutPassiveMotionFunc(passiveMotionGL)
glutKeyboardFunc(keyboardGL)
glutKeyboardUpFunc(keyboardUpGL)
glutReshapeFunc(reshapeGL)
glutJoystickFunc(joystickGL, 25)

glutTimerFunc(1000 // FPS, timerGL, 0)

glutMainLoop()
