#version 330 core

in vec3 fragColor;
in vec2 fragTexCoord;
in vec3 fragCoord;
in vec3 fragNormal;
in vec3 camPos;

in vec3 tangentPos;
in vec3 tangentLightPos;
in vec3 tangentViewPos;

in vec4 shadowCoord;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D texImage;
uniform sampler2D normalMap;

uniform sampler2D shadowMap;

const float heightScale = 0.25;

out vec4 color;

float ShadowCalculation() {
    // Perform perspective divide
    vec3 projCoords = shadowCoord.xyz / shadowCoord.w;
    vec2 uvCoords;
    uvCoords.x = projCoords.x * 0.5 + 0.5;
    uvCoords.y = projCoords.y * 0.5 + 0.5;
    float z = projCoords.z * 0.5 + 0.5;
    
    float depth = texture(shadowMap, uvCoords).x;
    
    float bias = 0.0025;

    if (depth + bias < z) {
        return 0.5;
    } else {
        return 1.0;
    }
}

void main() {
    // vec3 v = normalize(camPos - fragCoord);  
    vec3 v = normalize(tangentViewPos - tangentPos);
    // vec3 l = normalize(light.position - fragCoord);
    vec3 l = normalize(tangentLightPos - tangentPos);

    vec3 normal = texture(normalMap, fragTexCoord).rgb * 2.0 - 1.0;
    vec3 dif = texture(texImage, fragTexCoord).rgb;
    
    // vec3 n = normalize(fragNormal);
    vec3 n = normalize(normal);

    vec3 diffuse = max(0, dot(l, n)) * light.Id;

    vec3 r = reflect(-l, n);

    vec3 specular = pow(max(dot(v, r), 0), 16) * light.Is;

    float shadow = ShadowCalculation();

    vec3 result = (light.Ia + (diffuse + specular) * shadow) * dif;

    color = vec4(result, 1.0);

}
