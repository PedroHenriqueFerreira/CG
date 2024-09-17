#!/usr/bin/env python
from __future__ import division
from OpenGL.GL import *
import numpy as np
import math
import pygame
import textwrap
from PIL import Image

vertex_shader_source = textwrap.dedent("""\
    uniform mat4 uMVMatrix;
    uniform mat4 uPMatrix;
       
    attribute vec3 aVertex;
    attribute vec3 aNormal;
    attribute vec2 aTexCoord;
    
    varying vec2 vTexCoord;
    
    void main(){
       vTexCoord = aTexCoord;
       // Make GL think we are actually using the normal
       aNormal;
       gl_Position = (uPMatrix * uMVMatrix)  * vec4(aVertex, 1.0);
    }
    """)

fragment_shader_source = textwrap.dedent("""\
    uniform sampler2D sTexture;
    varying vec2 vTexCoord;
    void main(){
       gl_FragColor = texture2D(sTexture, vTexCoord);
    }
    """)

def load_program(vertex_source, fragment_source):
    vertex_shader = load_shader(GL_VERTEX_SHADER, vertex_source)
    if vertex_shader == 0:
        return 0

    fragment_shader = load_shader(GL_FRAGMENT_SHADER, fragment_source)
    if fragment_shader == 0:
        return 0

    program = glCreateProgram()

    if program == 0:
        return 0

    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)

    glLinkProgram(program)

    if glGetProgramiv(program, GL_LINK_STATUS, None) == GL_FALSE:
        glDeleteProgram(program)
        return 0

    return program

def load_shader(shader_type, source):
    shader = glCreateShader(shader_type)

    if shader == 0:
        return 0

    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS, None) == GL_FALSE:
        info_log = glGetShaderInfoLog(shader)
        print(info_log)
        glDeleteProgram(shader)
        return 0

    return shader

def load_texture(filename):
    img = Image.open(filename, 'r').convert("RGB")
    img_data = np.array(img, dtype=np.uint8)
    w, h = img.size

    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    return texture


def perspective(fovy, aspect, z_near, z_far):
    f = 1 / math.tan(math.radians(fovy) / 2)
    return np.array([
        [f / aspect,  0,                                   0,  0],
        [          0, f,                                   0,  0],
        [          0, 0, (z_far + z_near) / (z_near - z_far), -1],
        [          0, 0, (2*z_far*z_near) / (z_near - z_far),  0]
    ])

def rotate(angle, x, y, z):
    s = math.sin(math.radians(angle))
    c = math.cos(math.radians(angle))
    magnitude = math.sqrt(x*x + y*y + z*z)
    nc = 1 - c
      
    x /= magnitude
    y /= magnitude
    z /= magnitude

    return np.array([
        [     c + x**2 * nc, y * x * nc - z * s, z * x * nc + y * s, 0],
        [y * x * nc + z * s,      c + y**2 * nc, y * z * nc - x * s, 0],
        [z * x * nc - y * s, z * y * nc + x * s,      c + z**2 * nc, 0],
        [                 0,                  0,                  0, 1],
    ])

_vertices = [
    ( 1.000000, -1.000000, -1.000000),
    ( 1.000000, -1.000000,  1.000000),
    (-1.000000, -1.000000,  1.000000),
    (-1.000000, -1.000000, -1.000000),
    ( 1.000000,  1.000000, -0.999999),
    ( 0.999999,  1.000000,  1.000001),
    (-1.000000,  1.000000,  1.000000),
    (-1.000000,  1.000000, -1.000000),
]
_normals = [
    ( 0.000000, -1.000000,  0.000000),
    ( 0.000000,  1.000000,  0.000000),
    ( 1.000000,  0.000000,  0.000000),
    (-0.000000,  0.000000,  1.000000),
    (-1.000000, -0.000000, -0.000000),
    ( 0.000000,  0.000000, -1.000000),
]


_texcoords = [
    (0.250043, 0.749957),
    (0.250043, 0.500000),
    (0.500000, 0.500000),
    (0.500000, 0.250043),
    (0.250043, 0.250043),
    (0.250044, 0.000087),
    (0.500000, 0.999913),
    (0.250043, 0.999913),
    (0.000087, 0.749956),
    (0.000087, 0.500000),
    (0.500000, 0.749957),
    (0.749957, 0.500000),
    (0.500000, 0.000087),
    (0.749957, 0.749957),
]
_vertex_triangles = [
    (1, 2, 3),
    (7, 6, 5),
    (4, 5, 1),
    (5, 6, 2),
    (2, 6, 7),
    (0, 3, 7),
    (0, 1, 3),
    (4, 7, 5),
    (0, 4, 1),
    (1, 5, 2),
    (3, 2, 7),
    (4, 0, 7),
]

_texture_triangles = [
    ( 0,  1,  2),
    ( 3,  4,  5),
    ( 6,  7,  0),
    ( 8,  9,  1),
    ( 1,  4,  3),
    (10,  2, 11),
    (10,  0,  2),
    (12,  3,  5),
    (10,  6,  0),
    ( 0,  8,  1),
    ( 2,  1,  3),
    (13, 10, 11),
]

_normal_triangles = [
    (0, 0, 0),
    (1, 1, 1),
    (2, 2, 2),
    (3, 3, 3),
    (4, 4, 4),
    (5, 5, 5),
    (0, 0, 0),
    (1, 1, 1),
    (2, 2, 2),
    (3, 3, 3),
    (4, 4, 4),
    (5, 5, 5),
]

vertices = np.array([
    _vertices[index]
    for indices in _vertex_triangles
    for index in indices
])

normals = np.array([
    _normals[index]
    for indices in _normal_triangles
    for index in indices
])

texcoords = np.array([
    _texcoords[index]
    for indices in _texture_triangles
    for index in indices
])


if __name__ == "__main__":
    width, height = 800, 600
    pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE)

    glViewport(0, 0, width, height)
    projection_matrix = perspective(45, width/height, 0.1, 500)
    model_matrix = np.identity(4, dtype=np.float32)
    view_matrix = np.identity(4, dtype=np.float32)
    view_matrix[-1, :-1] = (0, 0, -10)

    program = load_program(vertex_shader_source, fragment_shader_source)

    uMVMatrix = glGetUniformLocation(program, "uMVMatrix")
    uPMatrix = glGetUniformLocation(program, "uPMatrix")
    sTexture = glGetUniformLocation(program, "sTexture")
       
    aVertex = glGetAttribLocation(program, "aVertex")
    aNormal = glGetAttribLocation(program, "aNormal")
    aTexCoord = glGetAttribLocation(program, "aTexCoord")

    glUseProgram(program)
    glEnableVertexAttribArray(aVertex)
    glEnableVertexAttribArray(aNormal)
    glEnableVertexAttribArray(aTexCoord)

    texture = load_texture("texture.png")

    glActiveTexture(GL_TEXTURE0);
    glBindTexture(GL_TEXTURE_2D, texture)
    glUniform1i(sTexture, 0)

    glEnable(GL_DEPTH_TEST)

    running = True
    while running:

        # model_matrix = np.dot(model_matrix, rotate(1, 1, 0.5, 0))

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glVertexAttribPointer(aVertex, 3, GL_FLOAT, GL_FALSE, 0, vertices)
        glVertexAttribPointer(aNormal, 3, GL_FLOAT, GL_FALSE, 0, normals)
        glVertexAttribPointer(aTexCoord, 2, GL_FLOAT, GL_FALSE, 0, texcoords)

        mv_matrix = np.dot(model_matrix, view_matrix)
        glUniformMatrix4fv(uMVMatrix, 1, GL_FALSE, mv_matrix)
        glUniformMatrix4fv(uPMatrix, 1, GL_FALSE, projection_matrix)

        glDrawArrays(GL_TRIANGLES, 0, len(vertices))


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.rel
                if any(event.buttons):
                    model_matrix = model_matrix.dot(rotate(y, -1, 0, 0)).dot(rotate(x, 0, -1, 0))