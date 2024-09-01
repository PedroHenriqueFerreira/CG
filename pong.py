from OpenGL.GL import *
from OpenGL.GLUT import *
import glm 

# constantes
FPS = 30    
FLAT = 1    
GOURAUD = 2

# variÃ¡veis globais
janelaLargura = 500                                              # largura da janela em pixels
janelaAltura = 500                                               # altura da janela em pixels
cameraPosition = glm.vec3(20, -10, 20)                           # posiÃ§Ã£o da cÃ¢mera
lightPosition = glm.vec3(5,5,5)                                  # posiÃ§Ã£o da fonte de luz pontual
lightSpin = True                                                 # indica se a fonte de luz gira em torno da superfÃ­cie ou nÃ£o
lightRotation = glm.rotate(glm.mat4(1.0), 0.01, glm.vec3(0,0,1)) # matriz de rotaÃ§Ã£o para girar a fonte de luz
lightAmbient = glm.vec3(0.1)                                     # propriedade ambiente da fonte de luz
lightDiffuse = glm.vec3(1.0)                                     # propriedade difusa da fonte de luz
lightSpecular = glm.vec3(1.0)                                    # propriedade especular da fonte de luz
surfaceSize = 20.0                                               # tamanho da lateral da superfÃ­cie
surfaceDivisions = 10                                            # qtd de subdivisÃµes das laterais da superfÃ­cie
surfaceAmbient = glm.vec3(0.1)                                   # propriedade ambiente do material da superfÃ­cie
surfaceDiffuse = glm.vec3(0,1,1)                                 # propriedade difusa do material da superfÃ­cie
surfaceSpecular = glm.vec3(0.5)                                  # propriedade especular do material da superfÃ­cie
surfaceShine = 128                                               # propriedade da especularidade do material da superfÃ­cie
shadingType = FLAT                                               # tipo de sombreamento

#FunÃ§Ã£o contendo configuraÃ§Ãµes iniciais
def inicio():
    glClearColor(0,0,0,1)
    glPointSize(5)
    glLineWidth(1)              # altera a largura das linhas para 1 pixel
    glEnable(GL_DEPTH_TEST)     # habilitando a remoÃ§Ã£o de faces que estejam atrÃ¡s de outras (remoÃ§Ã£o de faces traseiras)

#FunÃ§Ã£o que converte glm.mat4 em list<float>
def mat2list(M):
    matrix = []
    for i in range(0,4):
        matrix.append(list(M[i]))
    return matrix

# FunÃ§Ã£o que trata alteraÃ§Ãµes no tamanho da janela
def alteraJanela(largura, altura):
    global janelaLargura, janelaAltura, aspectRatio
    janelaLargura = largura
    janelaAltura = altura
    glViewport(0,0,largura,altura) # reserva a Ã¡rea inteira da janela para desenhar

# FunÃ§Ã£o que trata entrada de teclado
def teclado(key, x, y):
    global surfaceDivisions, shadingType, lightSpin
    if key == b'd':
        surfaceDivisions -= 1     # diminui a quantidade de subdivisÃµes da superfÃ­cie
    elif key == b'D':
        surfaceDivisions += 1     # aumenta a quantidade de subdivisÃµes da superfÃ­cie
    elif key == b'f':
        shadingType = FLAT        # define que o tipo de sombreamento usado serÃ¡ FLAT (uma cor por face)
    elif key == b'g':
        shadingType = GOURAUD     # define que o tipo de sombreamento usado serÃ¡ GOURAUD (uma cor por vÃ©rtice)
    elif key == b' ':
        lightSpin = not lightSpin # interrompe ou continua o giro da fonte de luz sobre a superfÃ­cie


#FunÃ§Ã£o que altera variÃ¡veis de translaÃ§Ã£o, escala e rotaÃ§Ã£o a cada frame e manda redesenhar a tela
def timer(v):
    global lightPosition
    
    glutTimerFunc(int(1000/FPS), timer, 0) 
    
    if lightSpin:                                                                # se o giro da fonte de luz estiver habilitado
        lightPosition = glm.vec3(lightRotation * glm.vec4(lightPosition, 1.0))   # aplicaÃ§Ã£o da rotaÃ§Ã£o sobre a posiÃ§Ã£o da fonte de luz para mantÃª-la em movimento

    glutPostRedisplay()

# Calcula a cor de sombreamento de um ponto usando o Modelo de IluminaÃ§Ã£o de Phong
def shading(point, normal):
    # reflexÃ£o ambiente
    shadeAmbient = lightAmbient * surfaceAmbient

    # reflexÃ£o difusa
    l = glm.normalize(lightPosition - point)
    n = glm.normalize(normal)
    shadeDiffuse = lightDiffuse * surfaceDiffuse * glm.max(0.0, glm.dot(l,n))

    # reflexÃ£o especular
    v = glm.normalize(cameraPosition - point)
    r = 2*glm.dot(n,l)*n - l
    shadeSpecular = lightSpecular * surfaceSpecular * glm.max(0, glm.dot(v,r) ** surfaceShine)

    # modelo de iluminaÃ§Ã£o de Phong
    shade = shadeAmbient + shadeDiffuse + shadeSpecular

    return shade

# Desenha superfÃ­cie calculando iluminaÃ§Ã£o por face (Sombreamento Flat)
def drawFlat():
    #desenhando uma grade de triÃ¢ngulos
    delta = surfaceSize / surfaceDivisions   #distÃ¢ncia entre um vÃ©rtice e o prÃ³ximo tanto na direÃ§Ã£o do eixo x, quanto na direÃ§Ã£o do eixo y
    glBegin(GL_TRIANGLES)
    for i in range(0,surfaceDivisions):    
        for j in range(0,surfaceDivisions):
            p1 = glm.vec3(0.0)
            p2 = glm.vec3(0.0)
            p3 = glm.vec3(0.0)
            p4 = glm.vec3(0.0)
            
            # a cada passo do laÃ§o, desenha-se um quadrado p1-p2-p3-p4 formado por dois triangulos p1-p2-p3 e p1-p3-p4
            p1.x = -surfaceSize/2 + i*delta         # ponto 1
            p1.y = -surfaceSize/2 + j*delta
            p2.x = -surfaceSize/2 + (i+1)*delta     # ponto 2
            p2.y = -surfaceSize/2 + j*delta
            p3.x = -surfaceSize/2 + (i+1)*delta     # ponto 3
            p3.y = -surfaceSize/2 + (j+1)*delta
            p4.x = -surfaceSize/2 + i*delta         # ponto 4
            p4.y = -surfaceSize/2 + (j+1)*delta
            
            # como todos os triÃ¢ngulos estÃ£o no plano xy, eles possuem a mesma normal (vÃ¡lido apenas para este caso especÃ­fico)
            normal = glm.vec3(0,0,1)    

            # desenhando o triÃ¢ngulo p1-p2-p3
            pc = (1.0/3.0)*(p1+p2+p3)     # calculando o centro do triÃ¢ngulo p1-p2-p3
            cor = shading(pc,normal)      # calculando o sombreamento do ponto pc
            glColor3f(cor.r,cor.g,cor.b)  # aplicando essa cor no desenho do triÃ¢ngulo p1-p2-p3
            glVertex3f(p1.x,p1.y,p1.z)
            glVertex3f(p2.x,p2.y,p2.z)
            glVertex3f(p3.x,p3.y,p3.z)

            # desenhando o triÃ¢ngulo p1-p3-p4
            pc = (1/3)*(p1+p3+p4)         # calculando o centro do triÃ¢ngulo p1-p3-p4
            cor = shading(pc,normal)      # calculando o sombreamento do ponto pc
            glColor3f(cor.r,cor.g,cor.b)  # aplicando essa cor no desenho do triÃ¢ngulo p1-p3-p4
            glVertex3f(p1.x,p1.y,p1.z)
            glVertex3f(p3.x,p3.y,p3.z)
            glVertex3f(p4.x,p4.y,p4.z)
    glEnd()

# Desenha superfÃ­cie calculando iluminaÃ§Ã£o por face (Sombreamento Gouraud)
def drawGouraud():
    #desenhando uma grade de triÃ¢ngulos
    delta = surfaceSize / surfaceDivisions   #distÃ¢ncia entre um vÃ©rtice e o prÃ³ximo tanto na direÃ§Ã£o do eixo x, quanto na direÃ§Ã£o do eixo y
    glBegin(GL_TRIANGLES)
    for i in range(0,surfaceDivisions):    
        for j in range(0,surfaceDivisions):
            p1 = glm.vec3(0.0)
            p2 = glm.vec3(0.0)
            p3 = glm.vec3(0.0)
            p4 = glm.vec3(0.0)
            
            # a cada passo do laÃ§o, desenha-se um quadrado p1-p2-p3-p4 formado por dois triangulos p1-p2-p3 e p1-p3-p4
            p1.x = -surfaceSize/2 + i*delta         # ponto 1
            p1.y = -surfaceSize/2 + j*delta
            p2.x = -surfaceSize/2 + (i+1)*delta     # ponto 2
            p2.y = -surfaceSize/2 + j*delta
            p3.x = -surfaceSize/2 + (i+1)*delta     # ponto 3
            p3.y = -surfaceSize/2 + (j+1)*delta
            p4.x = -surfaceSize/2 + i*delta         # ponto 4
            p4.y = -surfaceSize/2 + (j+1)*delta
            
            # como todos os triÃ¢ngulos estÃ£o no plano xy, eles possuem a mesma normal (vÃ¡lido apenas para este caso especÃ­fico)
            normal = glm.vec3(0,0,1)    

            # calculando o sombreando dos 4 vÃ©rtices do quadrado
            cor1 = shading(p1,normal) # calculando o sombreamento do ponto p1
            cor2 = shading(p2,normal) # calculando o sombreamento do ponto p2
            cor3 = shading(p3,normal) # calculando o sombreamento do ponto p3
            cor4 = shading(p4,normal) # calculando o sombreamento do ponto p4

            # desenhando o triÃ¢ngulo p1-p2-p3 (aplicando o sombreando de cada ponto individualmente)
            glColor3f(cor1.r,cor1.g,cor1.b) 
            glVertex3f(p1.x,p1.y,p1.z)
            glColor3f(cor2.r,cor2.g,cor2.b) 
            glVertex3f(p2.x,p2.y,p2.z)
            glColor3f(cor3.r,cor3.g,cor3.b) 
            glVertex3f(p3.x,p3.y,p3.z)

            # desenhando o triÃ¢ngulo p1-p3-p4 (aplicando o sombreando de cada ponto individualmente)
            glColor3f(cor1.r,cor1.g,cor1.b) 
            glVertex3f(p1.x,p1.y,p1.z)
            glColor3f(cor3.r,cor3.g,cor3.b) 
            glVertex3f(p3.x,p3.y,p3.z)
            glColor3f(cor4.r,cor4.g,cor4.b) 
            glVertex3f(p4.x,p4.y,p4.z)
    glEnd()

# FunÃ§Ã£o usada para redesenhar o conteÃºdo do frame buffer
def desenha():
    # Limpando frame buffer e depth buffer antes de cada frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Definindo a projeÃ§Ã£o
    glMatrixMode(GL_PROJECTION)
    aspectRatio = janelaLargura/janelaAltura
    matrizProjecao = glm.perspective(glm.radians(45.0), aspectRatio, 1, 100) 
    glLoadMatrixf(mat2list(matrizProjecao))                                  

    # Definindo a cÃ¢mera
    glMatrixMode(GL_MODELVIEW) 
    matrizCamera = glm.lookAt(cameraPosition, glm.vec3(0), glm.vec3(0,0,1)) 
    glLoadMatrixf(mat2list(matrizCamera))                              

    # Desenhando a superfÃ­cie com o sombremento escolhido (Flat ou Gouraud)
    if shadingType == FLAT:      drawFlat()     
    elif shadingType == GOURAUD: drawGouraud()  
    
    # Desenhando a fonte de luz (um simples ponto para poder localizÃ¡-la dentro da imagem)
    glColor3f(1,1,0)
    glBegin(GL_POINTS)
    glVertex3f(lightPosition.x, lightPosition.y, lightPosition.z)
    glEnd()

    glutSwapBuffers() 

#Corpo principal do cÃ³digo
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA) 
glutInitWindowSize(int(janelaLargura),int(janelaAltura))
glutInitWindowPosition(0,0)
glutCreateWindow("Modelo de Iluminacao de Phong")
inicio()
glutDisplayFunc(desenha)
glutReshapeFunc(alteraJanela)
glutKeyboardFunc(teclado)
glutTimerFunc(int(1000/FPS), timer, 0)
glutMainLoop()

