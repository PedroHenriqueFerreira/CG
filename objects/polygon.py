from OpenGL.GL import *
from OpenGL.GLUT import *

from objects.texture import Texture2D

from utils.triangle import Triangle

from structures.vector import Vec2, Vec3

from objects.vao import VAO
from objects.shader import Shader

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

import numpy as np
import glm

from settings import POLYGON_SHADER, SHADOW_SHADER

class Polygon:
    def __init__(
        self,
        map: 'Map',
        coords: list[Vec2],
        height: float,
        color: Vec3,
        texture: Texture2D, 
        normal_texture: Texture2D,
        texture_size: float
    ):
        self.map = map
        
        self.coords = coords
        self.height = height
        self.color = color
        self.texture = texture
        self.normal_texture = normal_texture
        self.texture_size = texture_size
        
        self.triangles: list[Vec3] = []
        self.colors: list[Vec3] = []
        self.normals: list[Vec3] = []
        self.tex_coords: list[Vec2] = []
        self.tangents: list[Vec3] = []
        
        self.vao: VAO | None = None
        self.shader = POLYGON_SHADER
        self.shadow_shader = SHADOW_SHADER
        
        self.gl_list = 0
    
    def load(self):
        if len(self.triangles) > 0:
            return
        
        if self.is_clockwise():
            coords = self.coords[::-1]
        else:
            coords = self.coords[:]

        while len(coords) >= 3:
            triangle = self.get_ear(coords)
            
            if triangle is None:
                break
            
            p1 = triangle.p1
            p2 = triangle.p2
            p3 = triangle.p3
            
            self.tex_coords.extend([
                p1 / self.texture_size, 
                p2 / self.texture_size, 
                p3 / self.texture_size
            ])
            
            p1 = p1.to_vec3(self.height)
            p2 = p2.to_vec3(self.height)
            p3 = p3.to_vec3(self.height)
            
            self.triangles.extend([p1, p2, p3])
            
            self.normals.extend([Vec3(0, 0, 1)] * 3)
            self.colors.extend([self.color] * 3)

        t1 = Vec2(0, 0)
        
        for prev, curr in zip(self.coords[:-1], self.coords[1:]):
            vector = curr - prev
            
            normal = vector.normalize()
            length = vector.length()
            
            t2 = Vec2(length, 0) / self.texture_size
            t3 = Vec2(length, self.height) / self.texture_size
            t4 = Vec2(0, self.height) / self.texture_size
            
            self.tex_coords.extend([t1, t2, t3, t1, t3, t4])
            
            p1 = prev.to_vec3(0)
            p2 = curr.to_vec3(0)
            p3 = curr.to_vec3(self.height)
            p4 = prev.to_vec3(self.height)
            
            self.triangles.extend([p1, p2, p3, p1, p3, p4])

            self.normals.extend([Vec3(-normal.y, normal.x, 0)] * 6)
            self.colors.extend([self.color] * 6)

        for i in range(0, len(self.triangles), 3):
            v0 = self.triangles[i]
            v1 = self.triangles[i + 1]
            v2 = self.triangles[i + 2]
            
            uv0 = self.tex_coords[i]
            uv1 = self.tex_coords[i + 1]
            uv2 = self.tex_coords[i + 2]
            
            delta_pos1 = v1 - v0
            delta_pos2 = v2 - v0
            
            delta_uv1 = uv1 - uv0
            delta_uv2 = uv2 - uv0
            
            uv_cross = delta_uv1.x * delta_uv2.y - delta_uv1.y * delta_uv2.x
            
            if uv_cross == 0:
                tangent = Vec3(1, 0, 0)
            else:
                tangent = (delta_pos1 * delta_uv2.y - delta_pos2 * delta_uv1.y) / uv_cross
            
            self.tangents.extend([tangent] * 3)

        self.vao = VAO(self.triangles, self.colors, self.normals, self.tex_coords, self.tangents)

    def draw(self):
        self.load()
        self.texture.load()
        self.normal_texture.load()
        self.shader.load()
        self.shadow_shader.load()
        self.make_shadow_map()
        
        # ---------------
        
        # glViewport(0, 0, 1024, 1024)
        # glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.depth_map_fbo)
        # glClear(GL_DEPTH_BUFFER_BIT)
        
        # glUseProgram(self.shadow_shader.id)
        
        # glUniformMatrix4fv(self.shadow_shader.get('projection'), 1, GL_FALSE, self.map.projection.matrix)
        # glUniformMatrix4fv(self.shadow_shader.get('light'), 1, GL_FALSE, self.map.light.matrix)
        
        # glBindVertexArray(self.vao.id)
        # glDrawArrays(GL_TRIANGLES, 0, len(self.triangles))
        # glBindVertexArray(0)
          
        # glUseProgram(0)
        # glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
        # glViewport(0, 0, 800, 800)
        # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # ----------
        
        glUseProgram(self.shader.id)
        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.normal_texture.id)
    
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.depth_map)
        
        glUniform1i(self.shader.get('texImage'), 0)
        glUniform1i(self.shader.get('normalMap'), 1)
        glUniform1i(self.shader.get("shadowMap"), 2)
        glUniform3fv(self.shader.get('lightPos'), 1, self.map.light.position.to_list())
        glUniform3fv(self.shader.get('camPos'), 1, self.map.camera.position.to_list())
        glUniform3fv(self.shader.get('light.position'), 1, self.map.light.position.to_list())
        glUniform3fv(self.shader.get('light.Ia'), 1, self.map.light.Ia.to_list())
        glUniform3fv(self.shader.get('light.Id'), 1, self.map.light.Id.to_list())
        glUniform3fv(self.shader.get('light.Is'), 1, self.map.light.Is.to_list())
        
        glUniformMatrix4fv(self.shader.get('camera'), 1, GL_FALSE, self.map.camera.matrix)
        glUniformMatrix4fv(self.shader.get('projection'), 1, GL_FALSE, self.map.projection.matrix)
        glUniformMatrix4fv(self.shader.get('light'), 1, GL_FALSE, self.map.light.matrix)
        
        glBindVertexArray(self.vao.id)
        glDrawArrays(GL_TRIANGLES, 0, len(self.triangles))
        glBindVertexArray(0) 
          
        glUseProgram(0)
        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def make_shadow_map(self):
        if hasattr(self, 'depth_map_fbo'):
            return
        
        # First we'll create a framebuffer object for rendering the depth map
        depth_map_fbo = glGenFramebuffers(1)
        
        # Next we create a 2D texture that we'll use as the framebuffer's depth buffer
        depth_map = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, depth_map)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, 1024, 1024, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        # With the generated depth texture we can attach it as the framebuffer's depth buffer
        glBindFramebuffer(GL_FRAMEBUFFER, depth_map_fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depth_map, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.depth_map_fbo = depth_map_fbo
        self.depth_map = depth_map
    
    def draw_________(self):
        if self.gl_list > 0:
            return glCallList(self.gl_list)
        
        self.load()
        self.texture.load()
        
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
        glBegin(GL_TRIANGLES)
        
        for p, c, n, t in zip(self.triangles, self.colors, self.normals, self.tex_coords):
            glNormal3f(n.x, n.y, n.z)
            glColor3f(c.x, c.y, c.z)
            glTexCoord2f(t.x, t.y)
            glVertex3f(p.x, p.y, p.z)
            
        glEnd()
        
        glBindTexture(GL_TEXTURE_2D, 0)
        glEndList()
    
    def draw_(self):    
        if self.gl_list > 0:
            return glCallList(self.gl_list)
        
        self.load()
        self.texture.load()
        
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
        glColor3f(self.color.x, self.color.y, self.color.z)
        
        glBegin(GL_TRIANGLES)
        
        glNormal3f(0, 0, 1)
        
        for point in self.triangles:
            glTexCoord2f(point.x / self.texture_size, point.y / self.texture_size)
            glVertex3f(point.x, point.y, self.height)
        
        glEnd()
        
        glBegin(GL_TRIANGLES)
        
        for prev, curr in zip(self.coords[:-1], self.coords[1:]):
            vector = curr - prev
            
            normal = vector.normalize()
            length = vector.length()
            
            glNormal3f(-normal.y, normal.x, 0)
            
            glTexCoord2f(0, 0)
            glVertex3f(prev.x, prev.y, 0)
            glTexCoord2f(length / self.texture_size, 0)
            glVertex3f(curr.x, curr.y, 0)
            glTexCoord2f(length / self.texture_size, self.height / self.texture_size)
            glVertex3f(curr.x, curr.y, self.height)
            
            glTexCoord2f(0, 0)
            glVertex3f(prev.x, prev.y, 0)
            glTexCoord2f(length / self.texture_size, self.height / self.texture_size)
            glVertex3f(curr.x, curr.y, self.height)           
            glTexCoord2f(0, self.height / self.texture_size)
            glVertex3f(prev.x, prev.y, self.height)
        
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
        glEndList()            

    def is_clockwise(self):
        ''' Checa se as coordenadas estão no sentido horário '''
        
        coords = self.coords
        
        sum = (coords[0].x - coords[len(coords) - 1].x) * (coords[0].y + coords[len(coords) - 1].y)

        for i in range(len(coords) - 1):
            sum += (coords[i + 1].x - coords[i].x) * (coords[i + 1].y + coords[i].y)

        return sum > 0

    def get_ear(self, coord: list[Vec2]):
        ''' Retorna o triângulo que é uma orelha no polígono '''
        
        size = len(coord)

        if size < 3:
            return None

        if size == 3:
            triangle = Triangle(*coord)
            del coord[:]
            return triangle

        for i in range(size):
            triangle = Triangle(coord[(i - 1) % size], coord[i % size], coord[(i + 1) % size])

            tritest = False
            if triangle.is_convex():
                for x in coord:
                    if triangle.contains(x):
                        tritest = True

                if not tritest:
                    del coord[i % size]
                    return triangle
                
        return None