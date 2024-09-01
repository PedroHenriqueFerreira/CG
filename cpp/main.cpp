#include <GL/glut.h>

/*
 * Programa bÃ¡sico para testar eventos de teclado na GLUT.
 * Um quadrado serÃ¡ desenhado.
 * O quadrado pode ser movido utilizando as teclas das setas
 * O quadrado pode mudar sua cor utilizando as teclas R (vermelho), G (verde) e B (azul)
 * A abordagem de usar valores booleanos para identificar que teclas estÃ£o pressionadas (setas) serve pra tratar vÃ¡rias teclas pressionadas ao mesmo tempo
 */

//VariÃ¡veis globais
float r =  1.0; //componente vermelha da cor do quadrado
float g =  0.0; //componente verde da cor do quadrado
float b =  0.0; //componente azul da cor do quadrado
float px = 0.0; //coordenada x do vÃ©rtice inferior esquerdo
float py = 0.0; //coordenada y do vÃ©rtice inferior esquerdo
bool  cima     = false; //indica se a tecla da seta pra cima estÃ¡ pressionada
bool  baixo    = false; //indica se a tecla da seta pra baixo estÃ¡ pressionada
bool  esquerda = false; //indica se a tecla da seta pra esquerda estÃ¡ pressionada
bool  direita  = false; //indica se a tecla da seta pra direita estÃ¡ pressionada

//Ã‰ uma boa prÃ¡tica criar uma funÃ§Ã£o para agrupar configuraÃ§Ãµes iniciais do OpenGL para o desenho a ser feito
void inicio(){
    glClearColor(1.0, 1.0, 1.0, 1.0); //indica qual cor serÃ¡ usada para limpar o frame buffer (normalmente usa uma cor de background)
}

//FunÃ§Ã£o indicada pra GLUT que serÃ¡ executada sempre que um evento de teclado que gere um caractere ASCII Ã© criado
void tecladoASCII(unsigned char key, int x, int y){
    switch(key){ //nesse tipo de evento, a tecla pressionada Ã© um caractere e pode ser acessada na instruÃ§Ã£o switch
        case 'r': 
        case 'R': r = 1 - r; break; //caso a tecla R seja pressionada, a componente vermelha Ã© ligada ou desligada
        case 'g': 
        case 'G': g = 1 - g; break; //caso a tecla G seja pressionada, a componente verde Ã© ligada ou desligada
        case 'b': 
        case 'B': b = 1 - b; break; //caso a tecla B seja pressionada, a componente azul Ã© ligada ou desligada
    }
    
    glutPostRedisplay(); //InstruÃ§Ã£o que indica pra GLUT que o frame buffer deve ser atualizado
}

//FunÃ§Ã£o indicada pra GLUT que serÃ¡ executada sempre que um evento de teclado a partir de uma tecla especial Ã© criado
void tecladoSpecial(int key, int x, int y){
    switch(key){                                     //os cÃ³digos das teclas especiais sÃ£o valores inteiros, entÃ£o podem ser usados no switch
        case GLUT_KEY_LEFT:  esquerda = true; break; //caso a seta esquerda seja pressionada, a coordenada x do ponto inferior esquerdo Ã© reduzida, deslocando o quadrado pra esquerda
        case GLUT_KEY_RIGHT: direita = true;  break; //caso a seta direita seja pressionada, a coordenada x do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra direita
        case GLUT_KEY_DOWN:  baixo = true;    break; //caso a seta pra baixo seja pressionada, a coordenada y do ponto inferior esquerdo Ã© reduzida, deslocando o quadrado pra baixo
        case GLUT_KEY_UP:    cima = true;     break; //caso a seta pra cima seja pressionada, a coordenada y do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra cima
    }
    glutPostRedisplay(); //InstruÃ§Ã£o que indica pra GLUT que o frame buffer deve ser atualizado
}

//FunÃ§Ã£o indicada pra GLUT que serÃ¡ executada sempre que um evento de teclado a partir de uma tecla especial Ã© criado
void tecladoSpecialUp(int key, int x, int y){
    switch(key){                                     //os cÃ³digos das teclas especiais sÃ£o valores inteiros, entÃ£o podem ser usados no switch
        case GLUT_KEY_LEFT:  esquerda = false; break; //caso a seta esquerda seja pressionada, a coordenada x do ponto inferior esquerdo Ã© reduzida, deslocando o quadrado pra esquerda
        case GLUT_KEY_RIGHT: direita = false;  break; //caso a seta direita seja pressionada, a coordenada x do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra direita
        case GLUT_KEY_DOWN:  baixo = false;    break; //caso a seta pra baixo seja pressionada, a coordenada y do ponto inferior esquerdo Ã© reduzida, deslocando o quadrado pra baixo
        case GLUT_KEY_UP:    cima = false;     break; //caso a seta pra cima seja pressionada, a coordenada y do ponto inferior esquerdo Ã© aumentada, deslocando o quadrado pra cima
    }
    glutPostRedisplay(); //InstruÃ§Ã£o que indica pra GLUT que o frame buffer deve ser atualizado
}

//FunÃ§Ã£o indicada na 'main' que serÃ¡ usada para redesenhar o conteÃºdo do frame buffer
void desenha(){
    glClear(GL_COLOR_BUFFER_BIT); 
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-10,10,-10,10,-1,1);
    
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    if(cima)    py += 0.1;
    if(baixo)   py -= 0.1;
    if(esquerda)px -= 0.1;
    if(direita) px += 0.1;

    //desenhando os eixos x e y
    glColor3f(0,0,0);
    glBegin(GL_LINES);
    glVertex2f(-10,  0);
    glVertex2f( 10,  0);
    glVertex2f(  0,-10);
    glVertex2f(  0, 10);
    glEnd();

    //desenhando o interior quadrado
    glColor3f(r,g,b);
    glBegin(GL_QUADS);
    glVertex2f(px  ,py  );
    glVertex2f(px+1,py  );
    glVertex2f(px+1,py+1);
    glVertex2f(px  ,py+1);
    glEnd();

    //desenhando as bordas do quadrado
    glColor3f(0,0,0);
    glBegin(GL_LINE_LOOP);
    glVertex2f(px  ,py  );
    glVertex2f(px+1,py  );
    glVertex2f(px+1,py+1);
    glVertex2f(px  ,py+1);
    glEnd();
    
    glFlush();  
}

int main(int argc, char** argv){
    glutInit(&argc,argv);                         
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);  
    glutInitWindowPosition(200,200);              
    glutInitWindowSize(700,700);                  
    glutCreateWindow("Evento de teclado");        
 
    inicio();
 
    glutDisplayFunc(desenha);            //indica que a funÃ§Ã£o 'desenha' deve ser chamada sempre que o frame buffer deve ser atualizado
    glutKeyboardFunc(tecladoASCII);      //indica que a funÃ§Ã£o 'tecladoASCII' deve ser chamada sempre que uma tecla gere um caractere ASCII Ã© pressionada
    glutSpecialFunc(tecladoSpecial);     //indica que a funÃ§Ã£o 'tecladoSpecial' deve ser chamada sempre que uma tecla especial Ã© pressionada (Esc, Ctrl, Setas do teclado, Enter, etc.)
    glutSpecialUpFunc(tecladoSpecialUp); //indica que a funÃ§Ã£o 'tecladoSpecial' deve ser chamada sempre que uma tecla especial Ã© liberada (Esc, Ctrl, Setas do teclado, Enter, etc.)
 
    glutMainLoop(); //mantÃ©m um laÃ§o interno para que a janela permaneÃ§a aberta
    
    return 0;
}