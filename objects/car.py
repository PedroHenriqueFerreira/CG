from OpenGL.GL import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

from random import choice

from structures.matrix import Mat2
from structures.vector import Vec2

from objects.texture import Texture2D
from objects.sound import Sound

from objects.obj import OBJ

class Car:
    def __init__(
        self,
        map: 'Map',
        pos: Vec2,
        pilot: bool,
        texture: Texture2D,
        size: float,
        circle_texture: Texture2D,
        circle_size: float,
        circle_min_size: float,
        circle_max_size: float,
        forward_size: float,
        backward_size: float,
        rotation_size: float,
        forward_sound: Sound,
        right_sound: Sound,
        left_sound: Sound,
        finish_sound: Sound,
    ):
        self.map = map
        self.pos = pos
        self.pilot = pilot
        self.texture = texture
        self.size = size
        self.circle_texture = circle_texture
        self.circle_size = circle_size
        self.circle_min_size = circle_min_size
        self.circle_max_size = circle_max_size
        self.forward_size = forward_size
        self.backward_size = backward_size
        self.rotation_size = rotation_size
        self.forward_sound = forward_sound
        self.right_sound = right_sound
        self.left_sound = left_sound
        self.finish_sound = finish_sound
        
        self.next_pos: Vec2 | None = None
        self.prev_pos: Vec2 | None = None

        self.random_pos: Vec2 | None = None

        self.i = Vec2(1, 0)
        self.j = Vec2(0, 1)
        
        self.loaded = False
        
        ##
        self.obj = OBJ('models/low/untitled.obj')

    def load(self):
        self.size = self.map.km_to_world(self.size)
        self.circle_size = self.map.percent_to_world(self.circle_size)
        self.circle_min_size = self.map.km_to_world(self.circle_min_size)
        self.circle_max_size = self.map.km_to_world(self.circle_max_size)

        self.forward_size = self.map.km_to_world(self.forward_size)
        self.backward_size = self.map.km_to_world(self.backward_size)

        self.loaded = True

    def auto(self):
        if self.map.my_car == self:
            if not self.map.path:
                return
            
            coords = self.map.path.coords
            
            nearest = self.pos.nearest(*coords)
            distance = Vec2.distance(nearest, self.pos)
            
            index = coords.index(nearest)
            
            if index == len(coords) - 1:
                return self.move_forward()
            
            next_index = index + 1            
            
            if distance < self.forward_size - 1e-8:
                angle = Vec2.angle(self.j, coords[next_index] - coords[index])
                
                if abs(angle) >= self.rotation_size:
                    if angle < 0:
                        return self.rotate_right()
                    else:
                        return self.rotate_left()
                 
            self.move_forward()
        else:
            nearest = self.pos.nearest(*self.map.graph.keys())
            distance = Vec2.distance(nearest, self.pos)
            
            if distance < self.forward_size - 1e-8:
                if not self.random_pos:
                    if len(self.map.graph[nearest]) == 2:
                        angle_0 = Vec2.angle(self.j, self.map.graph[nearest][0] - nearest)
                        angle_1 = Vec2.angle(self.j, self.map.graph[nearest][1] - nearest)
                        
                        if abs(angle_0) < abs(angle_1):
                            self.random_pos = self.map.graph[nearest][0]
                        else:
                            self.random_pos = self.map.graph[nearest][1]
                        
                    else:
                        self.random_pos = choice(self.map.graph[nearest])
                
                angle = Vec2.angle(self.j, self.random_pos - nearest)
                
                if abs(angle) >= self.rotation_size:
                    if angle < 0:
                        return self.rotate_right()
                    else:
                        return self.rotate_left()
                
            self.random_pos = None
            
            self.move_forward()

    def move(self, size: float):
        sign = 1 if size >= 0 else -1
        
        nearest = self.pos.nearest(*self.map.graph.keys())
        nearest_distance = Vec2.distance(nearest, self.pos)
        
        expected = None
        
        if nearest_distance < abs(size) - 1e-8:
            self.pos = nearest    

            rotation = float('inf')
            index = -1
            
            for i, neighbor in enumerate(self.map.graph[nearest]):
                angle = Vec2.angle(self.j * sign, neighbor - nearest) 
                
                if abs(angle) < abs(rotation):
                    rotation = angle
                    index = i
            
            if abs(rotation) < 45:                
                self.i = Mat2.rotation(rotation) * self.i
                self.j = Mat2.rotation(rotation) * self.j
                
                self.pos += self.j * size
                
                expected = self.map.graph[nearest][index]
                
        else:
            self.pos += self.j * size
            
        self.move_assistant(nearest, nearest_distance)
        
        if not expected:
            return 
        
        self.point_assistant(expected)
    
    def point_assistant(self, expected: Vec2):
        if self.map.my_car != self:
            return
        
        if self.next_pos and self.next_pos == expected:
            return
        
        self.next_pos = expected
                                    
        for point in self.map.points:
            if point.pos != self.next_pos:
                continue
            
            if point.sound:
                point.sound.play()
                point.blink()
    
    def move_assistant(self, nearest: Vec2, distance: float):
        if distance >= self.size:
            return
            
        if self.map.my_car != self:
            return
        
        if self.prev_pos and self.prev_pos == nearest:
            return
        
        self.prev_pos = nearest
        
        coords = self.map.path.coords
        
        if nearest not in coords:
            return
        
        if nearest == coords[-1]:
            self.finish_sound.play()
            
            self.map.path = None
            self.map.origin = None
            self.map.destiny = None
            self.map.my_car = None
            self.map.buttons = []
            
            return
        
        if len(self.map.graph[nearest]) == 2:
            return
        
        index = coords.index(nearest)
        next_index = index + 1
        
        angle = Vec2.angle(self.j, coords[next_index] - coords[index])
        
        if abs(angle) < 22.5:
            self.forward_sound.play()
        else:
            if angle < 0:
                self.right_sound.play()
            else:
                self.left_sound.play()
    
    def move_forward(self):
        return self.move(self.forward_size)

    def move_backward(self):
        return self.move(-1 * self.backward_size)

    def rotate(self, angle: float):
        nearest = self.pos.nearest(*self.map.graph.keys())
        distance = Vec2.distance(nearest, self.pos)
        
        if distance < self.size:
            self.pos = nearest
        
            self.i = Mat2.rotation(angle) * self.i
            self.j = Mat2.rotation(angle) * self.j

    def rotate_left(self):
        self.rotate(self.rotation_size)

    def rotate_right(self):
        self.rotate(-1 * self.rotation_size)

    def local_to_world_matrix(self):
        return [
            [self.i.x, self.i.y, 0, 0],
            [self.j.x, self.j.y, 0, 0],
            [0, 0, 1, 0],
            [self.pos.x, self.pos.y, 0, 1]
        ]

    def rotation_matrix(self):
        return [
            [self.i.x, self.i.y, 0, 0],
            [self.j.x, self.j.y, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    def draw(self):
        if not self.loaded:
            self.load()

        texture = self.circle_texture
        size = self.circle_size / self.map.scale

        if size < self.circle_min_size:
            texture = self.texture
            size = self.size

        elif size > self.circle_max_size:
            size = self.circle_max_size

        glPushMatrix()

        glMultMatrixf(self.local_to_world_matrix())
        glScalef(size, size, size)

        if texture == self.circle_texture:
            texture.load()
            glBindTexture(GL_TEXTURE_2D, texture.id)
        
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
            
            glRotatef(180, 0, 0, 1)
            glRotatef(90, 1, 0, 0)
            
            self.obj.draw()
        

        glPopMatrix()

