import sys
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Constants for the terrain size
WIDTH = 100
HEIGHT = 100

# Initialize the terrain height array
terrain = np.zeros((WIDTH, HEIGHT), dtype=float)

def generate_terrain():
    """Generates a simple sinusoidal terrain."""
    for x in range(WIDTH):
        for z in range(HEIGHT):
            # Simple height function
            terrain[x][z] = 10.0 * math.sin(x / 10.0) * math.cos(z / 10.0)

def init_opengl():
    """Sets up the OpenGL environment."""
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Light position and properties
    light_position = [50.0, 50.0, 50.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # Set up the projection and view matrices
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, 1.0, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(50.0, 50.0, 150.0, 50.0, 0.0, 50.0, 0.0, 1.0, 0.0)

def render_terrain():
    """Renders the terrain using triangle strips."""
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    for x in range(WIDTH - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for z in range(HEIGHT):
            # Calculate the normal (simple approximation)
            glNormal3f(0.0, 1.0, 0.0)
            
            # First vertex
            glVertex3f(x, terrain[x][z], z)
            
            # Second vertex
            glVertex3f(x + 1, terrain[x + 1][z], z)
        glEnd()

def display():
    """Main display function."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Render the terrain
    render_terrain()
    
    glutSwapBuffers()

def main():
    # Initialize GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b'Simple Terrain in OpenGL')

    # Generate terrain and initialize OpenGL settings
    generate_terrain()
    init_opengl()

    # Register the display function
    glutDisplayFunc(display)

    # Start the main loop
    glutMainLoop()

if __name__ == '__main__':
    main()