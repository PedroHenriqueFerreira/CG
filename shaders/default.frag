#version 330 core

const bool usingNormalMap = true;

struct Light {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

uniform Light light;
uniform Material material;

uniform sampler2D diffuseMap;
uniform sampler2D normalMap;

in vec3 fragPos;
in vec2 texCoords;
in vec3 fragNormal;

in vec3 tangentFragPos;
in vec3 tangentLightPos;
in vec3 tangentViewPos;

out vec4 FragColor;

void main() { 
    vec3 n = vec3(0.0);

    if (usingNormalMap) 
        n = normalize(texture(normalMap, texCoords).rgb * 2.0 - 1.0);
    else 
        n = normalize(fragNormal);

    vec3 l = normalize(tangentLightPos - tangentFragPos);
    vec3 v = normalize(tangentViewPos - tangentFragPos);
    vec3 r = reflect(-l, n);

    vec3 color = texture(diffuseMap, texCoords).rgb;

    vec3 ambient = 0.25 * color;
    vec3 diffuse = max(dot(l, n), 0) * color;
    vec3 specular = vec3(0.2) * pow(max(dot(v, r), 0), 32.0);

    FragColor = vec4((ambient + diffuse + specular), 1.0);
}
