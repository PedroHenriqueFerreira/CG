from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

from glm import vec3, mat4, transpose

from settings import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

class Shader:
    def __init__(self, app: 'Map', vertex_file_path: str, fragment_file_path: str):
        self.app = app # Instância do mapa
        
        self.id = self.load(vertex_file_path, fragment_file_path) # ID do shader
        
        self.params: dict[str, int] = {} # Parâmetros do shader
        
    def load(self, vertex_file_path: str, fragment_file_path: str):
        ''' Carrega o shader '''
        
        with open(vertex_file_path, 'r') as file:
            vertex_shader_source = file.read()
        with open(fragment_file_path, 'r') as file:
            fragment_shader_source = file.read()
        
        vs_id = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fs_id = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        
        return compileProgram(vs_id, fs_id)
    
    def use(self):
        ''' Usa o shader '''
        
        glUseProgram(self.id)
    
    def unuse(self):
        ''' Para de usar o shader '''
        
        glUseProgram(0)
    
    def get(self, param: str):
        ''' Retorna o ID de um parâmetro do shader '''
        
        if param not in self.params:
            self.params[param] = glGetUniformLocation(self.id, param)
        
        return self.params[param]

    def set(self, param: str, value):
        ''' Define um valor para um parâmetro do shader '''
        
        location = self.get(param)
        
        if isinstance(value, vec3):
            glUniform3fv(location, 1, value.to_list())
        elif isinstance(value, mat4):
            glUniformMatrix4fv(location, 1, GL_FALSE, value.to_list())
        elif isinstance(value, int):
            glUniform1i(location, value)
        else:
            glUniform1f(location, value)
        
class Shaders:
    def __init__(self, app: 'Map'):
        self.default = Shader(app, DEFAULT_SHADER_VERT_FILE, DEFAULT_SHADER_FRAG_FILE)
        self.skybox = Shader(app, SKYBOX_SHADER_VERT_FILE, SKYBOX_SHADER_FRAG_FILE)