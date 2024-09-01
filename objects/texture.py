from OpenGL.GL import *
from PIL import Image

from structures.vector import Vec3, Vec2

class Texture2D:
    ''' Represents a 2D texture. '''
    
    def __init__(
        self, 
        file: str, 
        filter: Constant = GL_LINEAR, 
        wrap: Constant = GL_MIRRORED_REPEAT,
        env: Constant = GL_COMBINE
    ):  
        self.file = file
        self.filter = filter
        self.wrap = wrap
        self.env = env
        
        self.id = 0
        
    def load(self):
        ''' Loads the texture. '''
        
        if self.id > 0:
            return
        
        self.id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.filter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.filter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.wrap)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.wrap)
        
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, self.env)
        
        image = Image.open(self.file).transpose(Image.FLIP_TOP_BOTTOM)
        
        width, height = image.size
        data = image.convert('RGBA').tobytes()
        
        glTexImage2D(
            GL_TEXTURE_2D, 
            0, 
            GL_RGBA, 
            width, 
            height, 
            0, 
            GL_RGBA, 
            GL_UNSIGNED_BYTE, 
            data
        )
        
        glBindTexture(GL_TEXTURE_2D, 0)

    def draw(self):
        ''' Draws the texture. '''
        
        self.load()
        
        glBindTexture(GL_TEXTURE_2D, self.id)
        
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

class TextureCubeMap:
    ''' Represents a cube texture. '''
    
    def __init__(
        self, 
        files: list[str],
        filter: Constant = GL_LINEAR,
        wrap: Constant = GL_CLAMP_TO_EDGE,
        env: Constant = GL_REPLACE
    ):
        self.files = files
        self.filter = filter
        self.wrap = wrap
        self.env = env
        
        self.id = 0
        
    def load(self):
        ''' Loads the texture. '''
        
        if self.id > 0:
            return
        
        self.id = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.id)
        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, self.filter)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, self.filter)        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, self.wrap)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, self.wrap)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, self.wrap)
        
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, self.env)
        
        for i, file in enumerate(self.files):
            image = Image.open(file).transpose(Image.FLIP_TOP_BOTTOM)
            
            width, height = image.size
            data = image.convert('RGBA').tobytes()
            
            GL_TEXTURE_CUBE_MAP_POSITIVE_X
            
            glTexImage2D(
                GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 
                0, 
                GL_RGBA, 
                width, 
                height, 
                0, 
                GL_RGBA, 
                GL_UNSIGNED_BYTE, 
                data
            )
