#version 330 core

layout (location = 0) in vec3 aPos; 
layout (location = 1) in vec3 aColor; 
layout (location = 2) in vec3 aNormal;
layout (location = 3) in vec2 aTexCoord;
layout (location = 4) in vec3 aTangent;

uniform mat4 projection;
uniform mat4 camera;
uniform mat4 light;

uniform vec3 lightPos;
uniform vec3 camPos;

out vec3 fragColor; 
out vec3 fragCoord;
out vec2 fragTexCoord;
out vec3 fragNormal;

out vec4 shadowCoord;

out vec3 tangentPos;
out vec3 tangentLightPos;
out vec3 tangentViewPos;


void main(){
    gl_Position = projection * camera * vec4(aPos, 1.0);

    fragColor = aColor;
    fragTexCoord = aTexCoord;
    fragCoord = aPos;
    fragNormal = aNormal;

    shadowCoord = projection * light * vec4(aPos, 1.0);

    vec3 T = normalize(aTangent);
    vec3 N = normalize(aNormal);
    vec3 B = normalize(cross(N, T));

    mat3 TBN = transpose(mat3(T, B, N));

    tangentPos = TBN * aPos;
    tangentLightPos = TBN * lightPos;
    tangentViewPos = TBN * camPos;
}
