from OpenGL.GL import *

from numpy import ndarray
from ctypes import c_void_p

class VertexArray:
    def __init__(self, data: ndarray):
        self.id, self.size = self.load(data)
        
    def load(self, data: ndarray) -> tuple[int, int]:
        raise NotImplementedError()
    
    def draw(self):
        glBindVertexArray(self.id)
        glDrawArrays(GL_TRIANGLES, 0, self.size)
        glBindVertexArray(0)

class DefaultVertexArray(VertexArray):
    def load(self, data: ndarray) -> tuple[int, int]:
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao) 
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
         
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 11 * 4, c_void_p(0))
        glEnableVertexAttribArray(0)
        
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 11 * 4, c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 11 * 4, c_void_p(6 * 4))
        glEnableVertexAttribArray(2)
        
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 11 * 4, c_void_p(8 * 4))
        glEnableVertexAttribArray(3)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        return vao, len(data) // 11

class SkyBoxVertexArray(VertexArray):
    def load(self, data: ndarray) -> tuple[int, int]:
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao) 
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
         
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, c_void_p(0))
        glEnableVertexAttribArray(0)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        return vao, len(data) // 3