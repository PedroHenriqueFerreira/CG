from OpenGL.GL import *

from objects.texture import TextureCubeMap
from structures.vector import Vec3

class SkyBox:
    ''' Represents a skybox. '''
    
    def __init__(
        self, 
        files: list[str],
    ):
        self.files = files
        
        self.texture = TextureCubeMap(files)
    
        self.size = 100
        
        self.gl_list = 0
    
    def draw(self):
        ''' Draw the skybox. '''
        
        if self.gl_list > 0:
            return glCallList(self.gl_list)
        
        glDisable(GL_LIGHTING)
        
        self.texture.load()
        
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_CUBE_MAP)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture.id)
        
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        
        # BOTTOM
        
        glTexCoord3f(-1, 1, -1)
        glVertex3f(-self.size, self.size, -self.size)
        
        glTexCoord3f(-1, -1, -1)
        glVertex3f(-self.size, -self.size, -self.size)
        
        glTexCoord3f(1, -1, -1)
        glVertex3f(self.size, -self.size, -self.size)
        
        glTexCoord3f(1, 1, -1)
        glVertex3f(self.size, self.size, -self.size)
        
        # LEFT
        
        glTexCoord3f(-1, -1,  1)
        glVertex3f(-self.size, -self.size, self.size)
        
        glTexCoord3f(-1, -1, -1)
        glVertex3f(-self.size, -self.size, -self.size)
        
        glTexCoord3f(-1, 1, -1)
        glVertex3f(-self.size, self.size, -self.size)
        
        glTexCoord3f(-1,  1,  1)
        glVertex3f(-self.size, self.size, self.size)
        
        # RIGHT
        
        glTexCoord3f(1, -1, -1)
        glVertex3f(self.size, -self.size, -self.size)
        
        glTexCoord3f(1, -1,  1)
        glVertex3f(self.size, -self.size,  self.size)
        
        glTexCoord3f(1,  1,  1)
        glVertex3f(self.size,  self.size, self.size)
        
        glTexCoord3f(1,  1, -1)
        glVertex3f(self.size, self.size, -self.size)
        
        # TOP
        
        glTexCoord3f(-1, -1,  1)
        glVertex3f(-self.size, -self.size, self.size)
        
        glTexCoord3f(-1,  1,  1)
        glVertex3f(-self.size, self.size, self.size)
        
        glTexCoord3f(1,  1,  1)
        glVertex3f(self.size, self.size, self.size)
                
        glTexCoord3f(1, -1,  1)
        glVertex3f(self.size, -self.size, self.size)
        
        # FRONT
        
        glTexCoord3f(-1, 1, -1)
        glVertex3f(-self.size, self.size, -self.size)
        
        glTexCoord3f(1,  1, -1)
        glVertex3f(self.size, self.size, -self.size)
        
        glTexCoord3f(1,  1,  1)
        glVertex3f(self.size, self.size, self.size)
        
        glTexCoord3f(-1,  1,  1)
        glVertex3f(-self.size, self.size, self.size)
        
        # BACK
        
        glTexCoord3f(-1, -1, -1)
        glVertex3f(-self.size, -self.size, -self.size)
        
        glTexCoord3f(-1, -1,  1)
        glVertex3f(-self.size, -self.size, self.size)
        
        glTexCoord3f(1, -1, 1)
        glVertex3f(self.size, -self.size, self.size)
        
        glTexCoord3f(1, -1, -1)
        glVertex3f(self.size, -self.size, -self.size) 
        
        glEnd()
        
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)   
        glDisable(GL_TEXTURE_CUBE_MAP)
        
        glEnable(GL_LIGHTING)
        
        glEndList()
