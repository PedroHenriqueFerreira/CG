#version 330 core

layout (location = 0) in vec3 aPos; 
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in vec3 aTangent;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

uniform vec3 lightPos;
uniform vec3 viewPos;

out vec3 fragPos;
out vec2 texCoords;

out vec3 tangentFragPos;
out vec3 tangentLightPos;
out vec3 tangentViewPos;

void main(){
    fragPos = vec3(model * vec4(aPos, 1.0));
    texCoords = aTexCoords;

    vec3 T = normalize(mat3(model) * aTangent);
    vec3 N = normalize(mat3(model) * aNormal);
    T = normalize(T - dot(T, N) * N);
    vec3 B = normalize(cross(N, T));

    mat3 TBN = transpose(mat3(T, B, N));

    tangentFragPos = TBN * aPos;
    tangentLightPos = TBN * lightPos;
    tangentViewPos = TBN * viewPos;

    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
