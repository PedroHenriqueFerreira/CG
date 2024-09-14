#version 330 core

in vec3 vcor; // recebendo a cor do vertex shader (já interpolada)

out vec4 fragColor; // saída principal do fragment shader (a cor do fragmento)

void main() {
    // aplicando um efeito na cor interpolada usando a coordenada do fragmento
    vec3 fcor = sin(10 * (3.14 / 90) * gl_FragCoord.x) * vcor; 
    // atribuindo essa cor alterada para a variável de saída
    fragColor = vec4(fcor, 1.0);                    
}
