from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from unidecode import unidecode

from structures.vector import Vec2

from settings import LINE_STRING_WIDTH

class Text:
    def __init__(self, value: str, size: float, coords: list[Vec2]):
        self.value = unidecode(value)
        self.size = size
        self.coords = coords
        
        self.coords_distance: list[float] = []
        self.coords_rotation: list[float] = []
        self.coords_width = 0
        
        self.chars_width: dict[str, float] = {}
        
        self.width = 0
        self.height = 0
        self.scale = 0
        
        self.loaded = False
        
    def load(self):
        if abs(Vec2.degrees(Vec2(1, 0), self.coords[-1] - self.coords[0])) > 90:
            self.coords = self.coords[::-1]
        
        for curr, next in zip(self.coords[:-1], self.coords[1:]):
            distance = Vec2.distance(curr, next)
            rotation = Vec2.degrees(Vec2(1, 0), next - curr)
            
            self.coords_distance.append(distance)
            self.coords_rotation.append(rotation)
                 
            self.coords_width += distance

        for c in self.value:
            width = glutStrokeWidth(GLUT_STROKE_MONO_ROMAN, ord(c))
            
            self.chars_width[c] = width
            self.width += width
            
        self.height = glutStrokeHeight(GLUT_STROKE_MONO_ROMAN)
        
        self.scale = self.size / self.height
        
        self.loaded = True
        
        self.test = Vec2(0, 0)
       
    def split(self, width: float, scale: float):
        start = (self.coords_width - width) / 2
        
        positions: list[Vec2] = []
        rotations: list[float] = []
        values: list[str] = []
      
        cum_distance = 0
        char_index = 0
      
        for rotation, distance, curr, next in zip(
            self.coords_rotation, 
            self.coords_distance, 
            self.coords[:-1], 
            self.coords[1:]
        ):
            prev_cum_distance = cum_distance
            cum_distance += distance
            
            if cum_distance < start:
                continue
                
            elif prev_cum_distance < start:
                expected = start - prev_cum_distance
                
                positions.append(curr + (next - curr) * expected / distance)
                rotations.append(rotation)
                
                max_cum_char_width = distance - expected
            elif char_index < len(self.value):
                positions.append(curr)
                rotations.append(rotation)
                
                max_cum_char_width = distance
            else:
                break
            
            value = ''
            cum_char_width = 0
            
            for char in self.value[char_index:]:
                char_width = self.chars_width[char] * self.scale / scale
                cum_char_width += char_width
                
                if cum_char_width > max_cum_char_width:
                    break
                
                value += char
                char_index += 1
                
            values.append(value)
        
        return positions, rotations, values
        
    def draw(self, map):
        if not self.value:
            return
        
        if not self.loaded:
            self.load()
        
        if self.height * self.scale / map.scale < LINE_STRING_WIDTH / 2:
            scale = (self.height * self.scale) / (LINE_STRING_WIDTH / 2)
        else:
            scale = map.scale
        
        # if map.scale < 5:
        #     scale = map.scale
        # else:
        #     scale = 5
        
        width = self.width * self.scale / scale
        
        if width > self.coords_width:
            return
       
        for p, r, v in zip(*self.split(width, scale)):
            glPushMatrix()
            
            glTranslatef(p.x, p.y, 0)
            glRotatef(r, 0, 0, 1)
            glScale(self.scale / scale, self.scale / scale, 1)
            
            glTranslatef(0, -self.height / 2, 0)
            
            for char in v.encode():
                glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, char)
            
            glPopMatrix()
