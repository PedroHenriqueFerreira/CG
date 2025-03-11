from OpenGL.GL import *
from OpenGL.GLU import *

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

from structures.vector import Vec2

from objects.texture import Texture2D

class Button:
    def __init__(
        self, 
        map: 'Map',
        pos: Vec2, 
        texture: Texture2D, 
        hover_texture: Texture2D, 
        width: float, 
        height: float,
        action: Callable[[], None]
    ):
        self.map = map
        self.pos = pos
        self.texture = texture
        self.hover_texture = hover_texture
        self.width = width
        self.height = height
        self.action = action
        
        self.hovered = False
        
        self.loaded = False
        
    def hover(self, mouse: Vec2):
        if (
            mouse.x > self.pos.x - self.width / 2 and mouse.x < self.pos.x + self.width / 2 and
            mouse.y > self.pos.y - self.height / 2 and mouse.y < self.pos.y + self.height / 2
        ):
            self.hovered = True
        else:
            self.hovered = False
       
    def click(self):
        self.action()
        
    def load(self):
        self.pos = self.map.pos_to_screen(self.pos)

        self.width = self.map.percent_to_world(self.width)
        self.height = self.map.percent_to_world(self.height)

        self.loaded = True

    def draw(self, aspect: float):        
        if not self.loaded:
            self.load()
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        
        glOrtho(-aspect, aspect, -1, 1, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glTranslatef(self.pos.x, self.pos.y, 0.01)
        glScalef(self.width, self.height, 1)

        if self.hovered:
            self.hover_texture.load()
            
            glBindTexture(GL_TEXTURE_2D, self.hover_texture.id)
        
            glBegin(GL_QUADS)
            
            glTexCoord2f(0, 0)
            glVertex3f(-0.5, -0.5, 0)
            
            glTexCoord2f(1, 0)
            glVertex3f(0.5, -0.5, 0)
            
            glTexCoord2f(1, 1)
            glVertex3f(0.5, 0.5, 0)
            
            glTexCoord2f(0, 1)
            glVertex3f(-0.5, 0.5, 0)
            
            glEnd()
            
            glBindTexture(GL_TEXTURE_2D, 0)
            
        else:
            self.texture.load()
            
            glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
            glBegin(GL_QUADS)
            
            glTexCoord2f(0, 0)
            glVertex3f(-0.5, -0.5, 0)
            
            glTexCoord2f(1, 0)
            glVertex3f(0.5, -0.5, 0)
            
            glTexCoord2f(1, 1)
            glVertex3f(0.5, 0.5, 0)
            
            glTexCoord2f(0, 1)
            glVertex3f(-0.5, 0.5, 0)
            
            glEnd()
            
            glBindTexture(GL_TEXTURE_2D, 0)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        