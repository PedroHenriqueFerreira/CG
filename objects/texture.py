from OpenGL.GL import *
from PIL import Image

class Texture:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
        self.id = 0
        
        self.load()
        
    def load(self):
        image = Image.open(self.filepath).transpose(Image.FLIP_TOP_BOTTOM)

        data = image.tobytes()
        
        width, height = image.size
        
        self.id = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, self.id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
        glBindTexture(GL_TEXTURE_2D, 0)
