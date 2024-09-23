from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

class Shader:
    def __init__(self, vertex_file_path: str, fragment_file_path: str):
        self.vertex_file_path = vertex_file_path
        self.fragment_file_path = fragment_file_path
        
        self.params: dict[str, int] = {}
        
        self.id = 0
        
    def load(self):
        if self.id != 0:
            return
        
        with open(self.vertex_file_path, 'r') as file:
            vertex_shader_source = file.read()
        with open(self.fragment_file_path, 'r') as file:
            fragment_shader_source = file.read()
        
        vs_id = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fs_id = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        
        self.id = compileProgram(vs_id, fs_id)
    
    def get(self, param: str):
        if param not in self.params:
            self.params[param] = glGetUniformLocation(self.id, param)
            
        return self.params[param]