from OpenGL.GL import *

from objects.texture import TextureCubeMap

class SkyBox:
    ''' Represents a skybox. '''
    
    def __init__(
        self, 
        files: list[str],
    ):
        self.files = files
        
        self.texture = TextureCubeMap(files)
        
        self.gl_list = 0
    
    def draw(self):
        ''' Draw the skybox. '''
        
        if self.gl_list > 0:
            return glCallList(self.gl_list)
        
        self.texture.load()
        
        self.gl_list = glGenLists(1)
        
        glNewList(self.gl_list, GL_COMPILE)
        
        glEnable(GL_TEXTURE_CUBE_MAP)
        
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture.id)
        
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        
        # BOTTOM
        
        glTexCoord3f(-1, 1, -1)
        glVertex3f(-2, 2, -2)
        
        glTexCoord3f(-1, -1, -1)
        glVertex3f(-2, -2, -2)
        
        glTexCoord3f(1, -1, -1)
        glVertex3f(2, -2, -2)
        
        glTexCoord3f(1, 1, -1)
        glVertex3f(2, 2, -2)
        
        # LEFT
        
        glTexCoord3f(-1, -1,  1)
        glVertex3f(-2, -2, 2)
        
        glTexCoord3f(-1, -1, -1)
        glVertex3f(-2, -2, -2)
        
        glTexCoord3f(-1, 1, -1)
        glVertex3f(-2, 2, -2)
        
        glTexCoord3f(-1,  1,  1)
        glVertex3f(-2, 2, 2)
        
        # RIGHT
        
        glTexCoord3f(1, -1, -1)
        glVertex3f(2, -2, -2)
        
        glTexCoord3f(1, -1,  1)
        glVertex3f(2, -2,  2)
        
        glTexCoord3f(1,  1,  1)
        glVertex3f(2,  2, 2)
        
        glTexCoord3f(1,  1, -1)
        glVertex3f(2, 2, -2)
        
        # TOP
        
        glTexCoord3f(-1, -1,  1)
        glVertex3f(-2, -2, 2)
        
        glTexCoord3f(-1,  1,  1)
        glVertex3f(-2, 2, 2)
        
        glTexCoord3f(1,  1,  1)
        glVertex3f(2, 2, 2)
                
        glTexCoord3f(1, -1,  1)
        glVertex3f(2, -2, 2)
        
        # FRONT
        
        glTexCoord3f(-1, 1, -1)
        glVertex3f(-2, 2, -2)
        
        glTexCoord3f(1,  1, -1)
        glVertex3f(2, 2, -2)
        
        glTexCoord3f(1,  1,  1)
        glVertex3f(2, 2, 2)
        
        glTexCoord3f(-1,  1,  1)
        glVertex3f(-2, 2, 2)
        
        # BACK
        
        glTexCoord3f(-1, -1, -1)
        glVertex3f(-2, -2, -2)
        
        glTexCoord3f(-1, -1,  1)
        glVertex3f(-2, -2, 2)
        
        glTexCoord3f(1, -1, 1)
        glVertex3f(2, -2, 2)
        
        glTexCoord3f(1, -1, -1)
        glVertex3f(2, -2, -2) 
        
        glEnd()
        
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)   
        
        glDisable(GL_TEXTURE_CUBE_MAP)
        
        glEndList()
