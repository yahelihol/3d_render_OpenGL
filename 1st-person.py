# View 3d environment 1st person

from draw_3d_shapes import *
from math import *

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

# Initialize Pygame

pygame.init()
WIDTH, HEIGHT = 1200, 900
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.mouse.set_visible(False)
# Set the initial camera position and rotation
camera_pos = [0, 2, 10]    # Camera position (x, y, z)
camera_pitch = 0.0       # Camera pitch (vertical rotation angle)
camera_yaw = 0.0         # Camera yaw (horizontal rotation angle)
zoom = 45
zoom_speed = 0.1
glEnable(GL_DEPTH_TEST)
# Function to set the camera perspective
def set_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, (WIDTH / HEIGHT), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(-camera_pitch, 1, 0, 0)
    glRotatef(-camera_yaw, 0, 1, 0)
    glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])

# Function to reset the mouse position to the center of the screen
def reset_mouse_position():
    pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)


def draw_crosshair():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(WIDTH//2 - 10, HEIGHT//2)
    glVertex2f(WIDTH//2 + 10, HEIGHT//2)
    glVertex2f(WIDTH//2, HEIGHT//2 - 10)
    glVertex2f(WIDTH//2, HEIGHT//2 + 10)
    glEnd()

time = 0
clock = pygame.time.Clock()
while True:
    time += 0.01
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll wheel up   # Zoom out
                zoom -= zoom_speed * 10
            elif event.button == 5:  # Scroll wheel down  # Zoom in
                zoom += zoom_speed * 10

    # Get the mouse movement
    mouse_rel = pygame.mouse.get_rel()
    sensitivity = 0.1 * zoom / 45.0
    mouse_rel = [x * sensitivity  for x in mouse_rel]  # Adjust the mouse sensitivity

    # Update the camera angles based on mouse movement
    camera_pitch -= mouse_rel[1]
    camera_yaw -= mouse_rel[0]

    camera_pitch = max(-90.0, min(90.0, camera_pitch))
    camera_yaw %= 360.0

    # Set the mouse position back to the center of the screen
    reset_mouse_position()

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Camera movement based on keyboard input
    speed = 0.1  # Adjust the movement speed
    forward = [
        -sin(radians(camera_yaw)),
        0,
        -cos(radians(camera_yaw))
    ]
    right = [
        -sin(radians(camera_yaw - 90)),
        0,
        -cos(radians(camera_yaw - 90))
    ]
    if keys[K_w]:
        camera_pos[0] += speed * forward[0]
        camera_pos[1] += speed * forward[1]
        camera_pos[2] += speed * forward[2]
    if keys[K_s]:
        camera_pos[0] -= speed * forward[0]
        camera_pos[1] -= speed * forward[1]
        camera_pos[2] -= speed * forward[2]
    if keys[K_a]:
        camera_pos[0] -= speed * right[0]
        camera_pos[1] -= speed * right[1]
        camera_pos[2] -= speed * right[2]
    if keys[K_d]:
        camera_pos[0] += speed * right[0]
        camera_pos[1] += speed * right[1]
        camera_pos[2] += speed * right[2]
    if keys[K_q] or keys[K_LSHIFT]:
        camera_pos[1] -= speed
    if keys[K_e] or keys[K_SPACE]:
        camera_pos[1] += speed
    if keys[K_ESCAPE]:
        pygame.quit()
        quit()
    if keys[pygame.K_r]:
        camera_pos = [0, 2, 10]  # Camera position (x, y, z)
        camera_pitch = 0.0  # Camera pitch (vertical rotation angle)
        camera_yaw = 0.0  # Camera yaw (horizontal rotation angle)
        zoom = 45
    pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)

    if keys[K_y]:  # Zoom out
        zoom -= zoom_speed
    if keys[K_t]:  # Zoom in
        zoom += zoom_speed
    zoom = max(10.1, min(119.9, zoom))

    # Set the camera perspective
    set_camera()
    # Clear the screen and draw your 3D objects here
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Draw your 3D scene

    glPushMatrix()
    glLineWidth(2.0)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(-3, 4):
        for j in range(-3, 4):
            draw_cube_w(i, 0, j, 1)
    draw_axis_arrows()
    glColor3f(1.0, 1.0, 1.0)
    draw_sphere(0.1, 40, 40)

    glTranslatef(0.0, 1.5, 1.9)
    glColor3f(0.6, 0.6, 0.9)
    glLineWidth(4.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # wireframe
    draw_octahedron()

    glTranslatef(0.0, 1.5, 1.9)
    glColor3f(0.1, 0.8, 0.6)

    draw_torus(2, 0.8, 32, 32)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Reset to normal after

    glPopMatrix()

    # 2D GUI section:
    glClear(GL_DEPTH_BUFFER_BIT)  # Make sure text renders above everything else
    set_2d(WIDTH, HEIGHT)
    draw_crosshair()
    # Draw GUI text
    draw_text(f"camera_x: {round(camera_pos[0], 1)}", 12, HEIGHT-30, 32)
    draw_text(f"camera_y: {round(camera_pos[1], 1)}", 12, HEIGHT-60, 32)
    draw_text(f"camera_z: {round(camera_pos[2], 1)}", 12, HEIGHT-90, 32)
    draw_text(f"camera_pitch: {round(camera_pitch, 1)}", 12, HEIGHT-120, 32)
    draw_text(f"camera_yaw: {round(camera_yaw, 1)}", 12, HEIGHT-150, 32)
    draw_text(f"zoom: {round(zoom, 1)}", 12, HEIGHT - 180, 32)
    draw_text(f"time: {round(time, 6)}", 12, HEIGHT-210, 32)
    draw_text(f"FPS: {round(clock.get_fps(), 1)}", 12, HEIGHT - 240, 32)

    pygame.display.flip()
    clock.tick(80)


#draw_text(f"camera_x: {round(camera_pos[0], 6)}", -1.6, 1.1, 32)
#    draw_text(f"camera_y: {round(camera_pos[1], 6)}", -1.6, 1.0, 32)
#    draw_text(f"camera_z: {round(camera_pos[2], 6)}", -1.6, 0.9, 32)
##    draw_text(f"camera_pitch: {round(camera_pitch, 6)}", -1.6, 0.8, 32)
 #   draw_text(f"camera_yaw: {round(camera_yaw, 6)}", -1.6, 0.7, 32)
 #   draw_text(f"time: {round(time, 6)}", -1.6, 0.6, 32)
