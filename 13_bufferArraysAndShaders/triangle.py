from OpenGL.GL import *
import numpy as np
import ctypes

class Triangle:
    def __init__(self):
        # dados do triângulo: coordenadas dos vértices e cores de cada vértice
        self.vertices = ( 
            -0.5, -0.5, 0.0,  1.0, 0.0, 0.0, # pos_x, pos_y, pos_z, cor_r, cor_g, cor_b
             0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
             0.0,  0.5, 0.0,  0.0, 0.0, 1.0
        )

        # conversão da lista em floats de 32 bits (exigência no Python, porque usa tipagem dinâmica)
        self.vertices = np.array(self.vertices, dtype=np.float32)

        # variável indicando a quantidade de vértices no buffer
        self.qtdVertices = 3

        self.vao = glGenVertexArrays(1) # criando um vertex array (espaço de memória para armazenar conteúdo de vérttices)
        glBindVertexArray(self.vao)     # tornando-o ativo

        # criando um vertex buffer
        self.vbo = glGenBuffers(1)              # criando um vertex buffer (espaço de memória gráfica que irá receber os dados dos vértices)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) # tornando esse buffer ativo

        # copiando todos os dados dos vértices da lista acima para o buffer recém-criado
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # informando como os dados dos vértices estão organizados dentro do buffer
        # Descrevendo a organização das posições de cada vértice
        glVertexAttribPointer(0,                   # o primeiro atributo por cada vértice tem código 0 (serão as posições)
                              3,                   # esse atributo possui três valores cada
                              GL_FLOAT,            # esses valores são do tipo float
                              GL_FALSE,            #
                              24,                  # entre os dados de uma posição para o próximo, há 24 bytes de espaço a ser pulado (6*4 bytes = 6 floats)
                              ctypes.c_void_p(0))  # endereço de memória contado do início do vertex array = iniciando no byte 0
        glEnableVertexAttribArray(0)               # habilitando esse parâmetro

        # Descrevendo a organização das cores de cada vértice
        glVertexAttribPointer(1,                   # o segundo atributo por cada vértice tem código 1 (serão as cores) 
                              3,                   # esse atributo possui três valores cada
                              GL_FLOAT,            # os valores desse atributo são do tipo float
                              GL_FALSE,            #
                              24,                  # entre os dados de uma cor para a próxima, há 24 bytes de espaço a ser pulado (6*4 bytes = 6 floats)
                              ctypes.c_void_p(12)) # endereço de memória contado do início do vertex array = iniciando no byte 12 (3*4 bytes = 3 floats)
        glEnableVertexAttribArray(1)               # habilitando esse parâmetro

        # Desabilitando o buffer e o vertex array (devem ser ativados apenas quando forem usados)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
