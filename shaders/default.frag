#version 330 core

uniform sampler2D diffuseMap;
uniform sampler2D normalMap;
uniform sampler2D displacementMap;

in vec3 fragPos;
in vec2 texCoords;

in vec3 tangentFragPos;
in vec3 tangentLightPos;
in vec3 tangentViewPos;

const float heightScale = -0.01;

vec2 ParallaxOcclusionMapping(vec3 v) {
    const float minLayers = 8;
    const float maxLayers = 32;
    float numLayers = mix(maxLayers, minLayers, max(dot(vec3(0.0, 0.0, 1.0), v), 0.0));

    float layerDepth = 1.0 / numLayers;
    float currentLayerDepth = 0.0;

    vec2 P = v.xy / v.z * heightScale;
    vec2 deltaTexCoords = P / numLayers;

    vec2  currentTexCoords = texCoords;
    float currentDepthMapValue = texture(displacementMap, currentTexCoords).r;

    while (currentLayerDepth < currentDepthMapValue) {
        currentTexCoords -= deltaTexCoords;
        currentDepthMapValue = texture(displacementMap, currentTexCoords).r;
        currentLayerDepth += layerDepth;
    }

    vec2 prevTexCoords = currentTexCoords + deltaTexCoords;

    float afterDepth  = currentDepthMapValue - currentLayerDepth;
    float beforeDepth = texture(displacementMap, prevTexCoords).r - currentLayerDepth + layerDepth;

    float weight = afterDepth / (afterDepth - beforeDepth);
    vec2 finalTexCoords = prevTexCoords * weight + currentTexCoords * (1.0 - weight);

    return finalTexCoords;
}

void main() { 
    // vec2 normalizedDeviceCoord = (fragPos.xy / fragPos.z) / 2.0 + 0.5;
	// vec3 reflectionTextureCoord = vec3(normalizedDeviceCoord.x, -normalizedDeviceCoord.y, 1);

    vec3 l = normalize(tangentLightPos - tangentFragPos);
    vec3 v = normalize(tangentViewPos - tangentFragPos);

    float height = texture(displacementMap, texCoords).r;

    vec2 newTexCoords = ParallaxOcclusionMapping(v);

    // 
    // int width_ = int(floor(texCoords.x));
    // int height_ = int(floor(texCoords.y));

    // float rest_x = texCoords.x - width_;
    // float rest_y = texCoords.y - height_;

    // if (rest_x < 0.0 || rest_y < 0.0 || rest_x > 1.0 || rest_y > 1.0) {
    //     discard;
    // }
    ///

    vec3 normal = texture(normalMap, newTexCoords).rgb;

    vec3 n = normalize(normal * 2.0 - 1.0);
    vec3 r = reflect(-l, n);

    vec3 color = texture(diffuseMap, newTexCoords).rgb;

    vec3 ambient = 0.4 * color;
    vec3 diffuse = max(dot(l, n), 0) * color;
    vec3 specular = 0.2 * pow(max(dot(v, r), 0), 32.0) * vec3(1.0);

    gl_FragColor = vec4((ambient + diffuse + specular), 1.0);
}
