#

import os
import subprocess


def install_dependencies():
    # Check if requirements.txt exists
    if os.path.isfile('requirements.txt'):
        # Install dependencies using pip
        try:
            subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
    else:
        print("No requirements.txt file found.")

# Install dependencies
install_dependencies()

# Now you can import the required libraries

import math

import pygame
import pygame.font
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *
from PIL import Image

# Your code that uses the libraries follows here

vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4]
]

def set_2d(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
def draw_text(text, x, y, font_size=24, color=(255, 255, 255), background_color=(0, 0, 0)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color, background_color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    glRasterPos2f(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def draw_rectangle(top_left, bottom_left, top_right, bottom_right):
    glBegin(GL_QUADS)
    glVertex3f(*top_left)  # Top left vertex
    glVertex3f(*top_right)    # Top right vertex
    glVertex3f(*bottom_right)      # Bottom right vertex
    glVertex3f(*bottom_left)    # Bottom left vertex
    glEnd()

def draw_sphere(radius, slices, stacks):
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, slices, stacks)


def draw_cylinder(radius, height, num_segments):
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        glVertex3f(x, y, height / 2)
        glVertex3f(x, y, -height / 2)
    glEnd()

    glBegin(GL_POLYGON)
    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        glVertex3f(x, y, height / 2)
    glEnd()

    glBegin(GL_POLYGON)
    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        glVertex3f(x, y, -height / 2)
    glEnd()


def draw_cube_w(x, y, z, size):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            v = (vertices[vertex][0] * 0.5 * size + x * size,
                        vertices[vertex][1] * 0.5 * size + y * size,
                        vertices[vertex][2] * 0.5 * size + z * size)
            glVertex3f(*v)
    glEnd()


def draw_cone(radius, height, num_segments):
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, height / 2)
    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, -height / 2)
    glEnd()

    glBegin(GL_POLYGON)
    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, -height / 2)
    glEnd()


def draw_torus(outer_radius, inner_radius, num_outer_segments, num_inner_segments):
    for i in range(num_outer_segments):
        glBegin(GL_QUAD_STRIP)
        for j in range(num_inner_segments + 1):
            for k in range(2):
                s = (i + k) % num_outer_segments + 0.5
                t = j % num_inner_segments

                x = (outer_radius + inner_radius * math.cos(s * 2.0 * math.pi / num_outer_segments)) * math.cos(t * 2.0 * math.pi / num_inner_segments)
                y = (outer_radius + inner_radius * math.cos(s * 2.0 * math.pi / num_outer_segments)) * math.sin(t * 2.0 * math.pi / num_inner_segments)
                z = inner_radius * math.sin(s * 2.0 * math.pi / num_outer_segments)

                glVertex3f(x, y, z)
        glEnd()



def draw_3d_arrow():
    glPushMatrix()
    draw_cylinder(.1, 1, 40)
    glTranslatef(0.0, 0.0, 0.6)
    draw_cone(.3, .5, 40)

    glPopMatrix()


def draw_axis_arrows():
    glPushMatrix()

    glTranslatef(0.5, 0.0, 0.0)
    glRotatef(90, 0, 1, 0)
    glColor3f(1.0, 0.0, 0.0)
    draw_cylinder(0.05, 1.0, 20)  # X-axis (Red)

    glPopMatrix()
    glPushMatrix()

    glTranslatef(0.0, 0.5, 0.0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 1.0, 0.0)
    draw_cylinder(0.05, 1.0, 20)  # Y-axis (Green)

    glPopMatrix()
    glPushMatrix()

    glTranslatef(0.0, 0.0, 0.5)
    glColor3f(0.0, 0.0, 1.0)
    draw_cylinder(0.05, 1.0, 20)  # Z-axis (Blue)

    glPopMatrix()


def draw_octahedron():
    # Vertices of the octahedron
    vertices = [
        [0.0, 1.0, 0.0],  # Top vertex
        [1.0, 0.0, 0.0],  # Right front vertex
        [0.0, 0.0, 1.0],  # Right back vertex
        [-1.0, 0.0, 0.0],  # Left back vertex
        [0.0, 0.0, -1.0],  # Left front vertex
        [0.0, -1.0, 0.0],  # Bottom vertex
    ]

    # Indices of the triangles
    triangles = [
        [0, 1, 2],  # Top-right
        [0, 2, 3],  # Top-left
        [0, 3, 4],  # Bottom-left
        [0, 4, 1],  # Bottom-right
        [5, 1, 2],  # Bottom-front
        [5, 2, 3],  # Bottom-back
        [5, 3, 4],  # Top-back
        [5, 4, 1],  # Top-front
    ]

    glBegin(GL_TRIANGLES)
    for triangle in triangles:
        for vertex_idx in triangle:
            glVertex3fv(vertices[vertex_idx])
    glEnd()
def draw_octahedron_w():
    # Vertices of the octahedron
    vertices = [
        (0.0, 1.0, 0.0),  # Top vertex
        (1.0, 0.0, 0.0),  # Right front vertex
        (0.0, 0.0, 1.0),  # Right back vertex
        (-1.0, 0.0, 0.0),  # Left back vertex
        (0.0, 0.0, -1.0),  # Left front vertex
        (0.0, -1.0, 0.0),  # Bottom vertex
    ]

    # Indices of the edges (pairs of vertex indices)
    edges = [
        (0, 1), (0, 2), (0, 3), (0, 4),  # Top edges
        (5, 1), (5, 2), (5, 3), (5, 4),  # Bottom edges
        (1, 2), (2, 3), (3, 4), (4, 1),  # Side edges
    ]

    glBegin(GL_LINES)
    for edge in edges:
        for vertex_idx in edge:
            glVertex3fv(vertices[vertex_idx])
    glEnd()


def draw_dodecahedron_w():  #   UNFINISHED, also Icosahedron
    phi = (1 + math.sqrt(5)) / 2

    # Vertices of a unit Dodecahedron
    vertices = [
        (1, 1, 1),
        (-1, 1, 1),
        (-1, -1, 1),
        (1, -1, 1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, -1),
        (0, 1 / phi, phi),
        (0, -1 / phi, phi),
        (0, -1 / phi, -phi),
        (0, 1 / phi, -phi),
        (phi, 0, 1 / phi),
        (phi, 0, -1 / phi),
        (-phi, 0, -1 / phi),
        (-phi, 0, 1 / phi),
        (1 / phi, phi, 0),
        (-1 / phi, phi, 0),
        (-1 / phi, -phi, 0),
        (1 / phi, -phi, 0),
    ]

    # Edges connecting the vertices to form the wireframe
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
        (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
        (0, 4), (1, 5), (2, 6), (3, 7),  # Connecting front and back faces
        (8, 9), (9, 10), (10, 11), (11, 8),  # Top face
        (12, 13), (13, 14), (14, 15), (15, 12),  # Bottom face
        (8, 12), (9, 13), (10, 14), (11, 15),  # Connecting top and bottom faces
        (0, 8), (1, 9), (2, 10), (3, 11),  # Connecting front and top faces
        (4, 12), (5, 13), (6, 14), (7, 15),  # Connecting back and bottom faces
    ]

    ccc  = [
    (1.0, 0.0, 0.0),   # Red
    (1.0, 0.5, 0.0),   # Orange
    (1.0, 1.0, 0.0),   # Yellow
    (0.5, 1.0, 0.0),   # Lime
    (0.0, 1.0, 0.0),   # Green
    (0.0, 1.0, 0.5),   # Turquoise
    (0.0, 1.0, 1.0),   # Cyan
    (0.0, 0.5, 1.0),   # Sky Blue
    (0.0, 0.0, 1.0),   # Blue
    (0.5, 0.0, 1.0),   # Purple
    (1.0, 0.0, 1.0),   # Magenta
    (1.0, 0.0, 0.5),   # Pink
    (0.95, 0.0, 0.95), # Light Magenta
    (0.75, 0.0, 0.75), # Lavender
    (0.5, 0.0, 0.5),   # Violet
    (0.75, 0.0, 0.25), # Plum
    (1.0, 0.0, 0.25),  # Ruby
    (0.9, 0.2, 0.0),   # Tangerine
    (0.75, 0.25, 0.0), # Burnt Orange
    (0.5, 0.25, 0.0)   # Brown
]



    #glBegin(GL_LINES)
    #for edge in edges:
    #    for vertex in edge:
    #        glVertex3fv(vertices[vertex])
    #glEnd()
    aaa= 0
    for vertex in vertices:

        glPushMatrix()
        glTranslatef(*vertex)
        glColor3f(ccc[aaa][0],ccc[aaa][1],ccc[aaa][2])
        draw_sphere(.1,20,20)
        glPopMatrix()
        aaa += 1


def draw_ellipsoid(radius_x, radius_y, radius_z, num_segments):
    pass

