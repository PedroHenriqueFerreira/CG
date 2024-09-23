#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

uniform mat4 camera;
uniform mat4 projection;
uniform mat4 light;

void main()
{
    vec4 FragPos = vec4(aPos, 1.0);
    gl_Position = projection * light * FragPos; // Standard MVP for rendering
}