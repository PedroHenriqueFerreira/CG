from OpenGL.GL import *
from OpenGL.GLUT import *
from triangle import *
from myShader import *

T = 0
shader = 0

# Função de inicialização
def inicio():
    global T, shader
    glClearColor(0,0,0,1)
    shader = MyShader('vertex.glsl','fragment.glsl') # criando objeto do tipo shader
    T = Triangle()                                   # criando objeto do tipo triângulo

def desenha():
    # limpando o frame buffer
    glClear(GL_COLOR_BUFFER_BIT)

    # desenhando
    glUseProgram(shader.shaderId)                # ativando o shader que irá definir como o triângulo será renderizado
    glBindVertexArray(T.vao)                     # ativando o vertex array contendo os dados do triângulo
    glDrawArrays(GL_TRIANGLES, 0, T.qtdVertices) # definindo que os dados contidos no buffer serão renderizados com a primitiva GL_TRIANGLES
    glBindVertexArray(0)                         # desativando o vertex array

    # atualizando a tela
    glFlush()

# corpo principal do código
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500,500)
glutInitWindowPosition(0,0)
glutCreateWindow('13 - Buffer Arrays e Shaders')
inicio()
glutDisplayFunc(desenha)
glutMainLoop()