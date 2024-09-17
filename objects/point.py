from OpenGL.GL import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

from objects.texture import Texture2D
from objects.sound import Sound

from structures.vector import Vec2

class Point:
    def __init__(
        self,
        map: 'Map',
        pos: Vec2,
        texture: Texture2D,
        size: float,
        min_size: float,
        max_size: float,
        max_blink_scale: float,
        delta_blink_scale: float,
        max_blink_times: int,
        sound: Sound | None = None,
    ):
        self.map = map
        self.pos = pos
        self.texture = texture
        self.size = size
        self.min_size = min_size
        self.max_size = max_size
        self.sound = sound
        self.max_blink_scale = max_blink_scale
        self.delta_blink_scale = delta_blink_scale
        self.max_blink_times = max_blink_times
        
        self.blink_times = 0

        self.blink_sign = 0
        self.blink_scale = 1
        self.blink_times = 0

        self.loaded = False
        
        self.counter = 0

    def load(self):
        self.size = self.map.percent_to_world(self.size)
        self.min_size = self.map.km_to_world(self.min_size)
        self.max_size = self.map.km_to_world(self.max_size)

        self.loaded = True

    def blink(self):
        self.blink_sign = 1
        self.blink_scale = 1
        
        self.blink_times = 0

    def draw(self):
        self.counter += 1
        
        if not self.loaded:
            self.load()
            self.texture.load()

        size = self.size / self.map.scale

        if size < self.min_size:
            size = self.min_size
        elif size > self.max_size:
            size = self.max_size

        if self.blink_sign == 1 and self.blink_scale >= self.max_blink_scale:
            self.blink_sign = -1
        elif self.blink_sign == -1 and self.blink_scale <= 1:
            self.blink_sign = 1
            
            self.blink_times += 1
            
            if self.blink_times >= self.max_blink_times:
                self.blink_sign = 0
            
        if self.blink_sign != 0:
            self.blink_scale += self.delta_blink_scale * self.blink_sign
        
        glPushMatrix()
        
        glTranslatef(self.pos.x, self.pos.y, 0)
        glScalef(
            size * self.blink_scale, 
            size * self.blink_scale, 
            size * self.blink_scale
        )

        glRotatef(self.counter * 10, 0, 0, 1)

        glTranslatef(0, 0, 0.5)    
        glRotatef(90, 1, 0, 0)
    
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
