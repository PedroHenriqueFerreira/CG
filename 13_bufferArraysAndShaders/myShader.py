from OpenGL.GL import *
import OpenGL.GL.shaders as gls

class MyShader:
    def __init__(self,vertexShaderFilePath, fragmentShaderFilePath):
        #lendo o arquivo do vertex shader
        with open(vertexShaderFilePath, 'r') as file:
            vertexShaderSource = file.read()
        #lendo o arquivo do fragment shader
        with open(fragmentShaderFilePath, 'r') as file:
            fragmentShaderSource = file.read()
        
        # compilando o vertex shader
        vsId = gls.compileShader(vertexShaderSource, GL_VERTEX_SHADER)      
        # compilando o fragment shader
        fsId = gls.compileShader(fragmentShaderSource, GL_FRAGMENT_SHADER)  
        # linkando ambos em um único programa gráfico
        self.shaderId = gls.compileProgram(vsId,fsId)                       



        

