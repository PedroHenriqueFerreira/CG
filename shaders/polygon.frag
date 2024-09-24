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

out vec4 FragColor;

float ShadowCalculation() {
    // perform perspective divide
    vec3 projCoords = (shadowCoord.xyz / shadowCoord.w);
    // transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;
    // get closest depth value from light's perspective (using [0,1] range fragPosLight as coords)
    float closestDepth = texture(shadowMap, projCoords.xy).r; 
    // get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    // check whether current frag pos is in shadow
    float shadow = currentDepth > closestDepth  ? 1.0 : 0.0;

    return shadow;
}

void main() {
    // vec3 v = normalize(camPos - fragCoord);  
    vec3 v = normalize(tangentViewPos - tangentPos);
    // vec3 l = normalize(light.position - fragCoord);
    vec3 l = normalize(tangentLightPos - tangentPos);

    vec3 normal = texture(normalMap, fragTexCoord).rgb * 2.0 - 1.0;
    vec3 color = texture(texImage, fragTexCoord).rgb;
    
    // vec3 n = normalize(fragNormal);
    vec3 n = normalize(normal);

    vec3 diffuse = max(0, dot(l, n)) * light.Id;

    vec3 r = reflect(-l, n);

    vec3 specular = pow(max(dot(v, r), 0), 16) * light.Is;

    float shadow = ShadowCalculation();

    vec3 result = (light.Ia + (diffuse + specular) * (1)) * color;

    FragColor = vec4(result, 1.0);
}
