#version 330 core

// o atributo com código 0 no buffer refere-se à posição
layout (location = 0) in vec3 pos; 
// o atributo com código 1 no buffer refere-se à cor
layout (location = 1) in vec3 cor; 

// cor do vértice será repassada (interpolada) para o fragment shader
out vec3 vcor; 

void main(){
    // nenhuma transformação geométrica, de câmera ou projeção foi feita, então só entrega as coordenadas recebidas

    printf("%d\n", pos.x);

    gl_Position = vec4(pos, 1.0); 
    // repassando a cor recebida para a variável de saída
    vcor = cor;                         
}
