from OpenGL.GL import *

from PIL import Image

from settings import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

class Textures:
    ''' Classe que representa as texturas do jogo. '''
    
    def __init__(self, app: 'Map'):
        self.app = app
        
        self.building_diffuse = Texture2D(BUILDING_DIFFUSE_TEXTURE_FILE)
        self.building_normal = Texture2D(BUILDING_NORMAL_TEXTURE_FILE)
        self.building_displacement = Texture2D(BUILDING_DISPLACEMENT_TEXTURE_FILE)
        
        self.water_diffuse = Texture2D(WATER_DIFFUSE_TEXTURE_FILE)
        self.water_normal = Texture2D(WATER_NORMAL_TEXTURE_FILE)
        self.water_displacement = Texture2D(WATER_DISPLACEMENT_TEXTURE_FILE)
        
        self.grass_diffuse = Texture2D(GRASS_DIFFUSE_TEXTURE_FILE)
        self.grass_normal = Texture2D(GRASS_NORMAL_TEXTURE_FILE)
        self.grass_displacement = Texture2D(GRASS_DISPLACEMENT_TEXTURE_FILE)

        self.unknown_diffuse = Texture2D(UNKNOWN_DIFFUSE_TEXTURE_FILE)
        self.unknown_normal = Texture2D(UNKNOWN_NORMAL_TEXTURE_FILE)
        self.unknown_displacement = Texture2D(UNKNOWN_DISPLACEMENT_TEXTURE_FILE)
        
        self.road_diffuse = Texture2D(ROAD_DIFFUSE_TEXTURE_FILE)
        self.road_normal = Texture2D(ROAD_NORMAL_TEXTURE_FILE)
        self.road_displacement = Texture2D(ROAD_DISPLACEMENT_TEXTURE_FILE)
        
        self.path_diffuse = Texture2D(PATH_DIFFUSE_TEXTURE_FILE)
        self.path_normal = Texture2D(PATH_NORMAL_TEXTURE_FILE)
        self.path_displacement = Texture2D(PATH_DISPLACEMENT_TEXTURE_FILE)

        self.ground_diffuse = Texture2D(GROUND_DIFFUSE_TEXTURE_FILE)
        self.ground_normal = Texture2D(GROUND_NORMAL_TEXTURE_FILE)
        self.ground_displacement = Texture2D(GROUND_DISPLACEMENT_TEXTURE_FILE)

        self.skybox = TextureCubeMap(SKYBOX_TEXTURE_FILES)
        
class Texture2D:
    ''' Classe que representa uma textura 2D. '''

    def __init__(self, file: str):  
        self.file = file
        
        self.id = self.load()
        
    def use(self, unit: int):
        ''' Usa a textura. '''
        
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.id)
        
    def unuse(self):
        ''' Para de usar a textura. '''

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)
        
    def load(self):
        ''' Carrega a textura. '''
        
        tex = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, tex)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE)
        
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
        
        glGenerateMipmap(GL_TEXTURE_2D)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        
        return tex

class TextureCubeMap:
    ''' Classe que representa uma textura cubemap. '''
    
    def __init__(self, files: list[str]):
        self.files = files
        
        self.id = self.load()
        
    def use(self, unit: int):
        ''' Usa a textura. '''
        
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.id)
        
    def unuse(self):
        ''' Para de usar a textura. '''

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
        
    def load(self):
        ''' Carrega a textura. '''
        
        tex = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_CUBE_MAP, tex)
        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        
        for i, file in enumerate(self.files):
            image = Image.open(file)
            
            if i in (0, 3, 5):
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                
            if i in (1, 2, 4):
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            
            if i in (0, 1):
                image = image.transpose(Image.ROTATE_90)
            
            width, height = image.size
            data = image.convert('RGBA').tobytes()
            
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

        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)
        
        return tex