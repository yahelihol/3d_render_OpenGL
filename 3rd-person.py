# View x by y by z grid centered 3d 3rd person

# import draw_3d_shapes
from draw_3d_shapes import *
from math import *

import pygame
import pygame.font
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

grid_size = (5, 9, 1)

cube_rotate_x = 0.0
cube_rotate_y = 0.0

time = 0
cube_size = 1.0


def draw_grid():
    glLineWidth(2.0)
    glColor3fv((1.0, 1.0, 1.0))
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            for z in range(grid_size[2]):
                draw_cube_w(x-0.5*(grid_size[0]-1), y-0.5*(grid_size[1]-1), z-0.5*(grid_size[2]-1), cube_size)

def draw():
    draw_grid()

    # draw_Rotating_Arrow()
    glColor3fv((1.0, 1.0, 1.0))
    draw_sphere(0.1, 40, 40)

    draw_axis_arrows()

    # draw 3 3d arrows of xyz
    # glColor3fv((1.0, 1.0, 1.0))
    # glColor3fv((1.0, 0.0, 0.0))
    # draw_sphere(0.1, 40, 40)
    # glColor3fv((1.0, 1.0, 0.0))
    # draw_3d_arrow()
    # glRotatef(-90, 1, 0, 0)
    # glColor3fv((1.0, 0.5, 0.0))
    # draw_3d_arrow()
    # glRotatef(90, 0, 1, 0)
    # glColor3fv((0.5, 0.5, 1.0))
    # draw_3d_arrow()
    # Draw a rectangle in the bottom right corner
    # rect_width = 2.0  # Adjust the rectangle size as needed
    # rect_height = 1.0
    # glBegin(GL_QUADS)
    # glColor3f(1.0, 0.0, 0.0)  # Set the color (in this case, red)
    # glVertex3f(grid_size * cube_size - rect_width, 0.0, grid_size * cube_size - rect_height)
    # glVertex3f(grid_size * cube_size - rect_width, 0.0, grid_size * cube_size)
    # glVertex3f(grid_size * cube_size, 0.0, grid_size * cube_size)
    # glVertex3f(grid_size * cube_size, 0.0, grid_size * cube_size - rect_height)
    # glEnd()




def get_camera_direction():
    # Compute direction vectors for the global X, Y, and Z axes based on camera orientation
    y_rad = radians(cube_rotate_y)
    x_rad = radians(cube_rotate_x)
    forward_x = -sin(y_rad) * cos(x_rad)
    forward_y = sin(x_rad)
    forward_z = -cos(y_rad) * cos(x_rad)
    right_x = cos(y_rad)
    right_z = sin(y_rad)
    return forward_x, forward_y, forward_z, right_x, right_z


def main():
    pygame.init()
    display = (1200, 900)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glEnable(GL_DEPTH_TEST)

    #glTranslatef(0.0, 0.0, -grid_size[2]* cube_size)

    clock = pygame.time.Clock()
    cube_rotate_x = 0.0
    cube_rotate_y = 0.0

    # Camera position
    camera_x = 0.0
    camera_y = 0.0
    camera_z = -2.0

    mouse_sensitivity = 0.2

    dragging = False
    last_mouse_pos = None

    while True:
        global time
        time += 0.01

        forward_x, forward_y, forward_z, right_x, right_z = get_camera_direction()
        camera_speed = 0.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll wheel up
                    camera_x -= forward_x
                    camera_y -= forward_y
                    camera_z -= forward_z
                elif event.button == 5:  # Scroll wheel down
                    camera_x += forward_x
                    camera_y += forward_y
                    camera_z += forward_z

        if dragging:
            mouse_pos = pygame.mouse.get_pos()
            if last_mouse_pos is not None:
                dx, dy = mouse_pos[0] - last_mouse_pos[0], mouse_pos[1] - last_mouse_pos[1]
                cube_rotate_y += dx * mouse_sensitivity
                cube_rotate_x += dy * mouse_sensitivity
            last_mouse_pos = mouse_pos
        else:
            last_mouse_pos = None
        # Camera movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            camera_y += camera_speed
        if keys[pygame.K_w]:
            camera_y -= camera_speed
        if keys[pygame.K_a]:
            camera_x += right_x * camera_speed
            camera_z += right_z * camera_speed
        if keys[pygame.K_d]:
            camera_x -= right_x * camera_speed
            camera_z -= right_z * camera_speed
        if keys[pygame.K_q] or keys[K_LSHIFT]:
            camera_x += forward_x * camera_speed
            camera_y += forward_y * camera_speed
            camera_z += forward_z * camera_speed
        if keys[pygame.K_e] or keys[K_SPACE]:
            camera_x -= forward_x * camera_speed
            camera_y -= forward_y * camera_speed
            camera_z -= forward_z * camera_speed
        if keys[pygame.K_r]:
            camera_x = 0.0
            camera_y = 0.0
            camera_z = -2.0
            cube_rotate_x = 0.0
            cube_rotate_y = 0.0
        if keys[K_ESCAPE]:
            pygame.quit()
            quit()

        camera_z = min(camera_z, 0.0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(camera_x, camera_y, camera_z)
        glRotatef(cube_rotate_x, 1, 0, 0)
        glRotatef(cube_rotate_y, 0, 1, 0)
        draw()
        glPopMatrix()


        glDisable(GL_DEPTH_TEST)
        glPushMatrix()
        glTranslatef(0.0, 0.0, -3)
        #draw_rectangle((0.7, -0.7, 0), (0.7, -1.3, 0), (1.7, -0.7, 0), (1.7, -1.3, 0))
        draw_text(f"camera_x: {round(camera_x, 6)}", -1.6, 1.1, 32)
        draw_text(f"camera_y: {round(camera_y, 6)}", -1.6, 1.0, 32)
        draw_text(f"camera_z: {round(camera_z, 6)}", -1.6, 0.9, 32)
        draw_text(f"cube_rotate_x: {round(cube_rotate_x, 6)}", -1.6, 0.8, 32)
        draw_text(f"cube_rotate_y: {round(cube_rotate_y, 6)}", -1.6, 0.7, 32)
        draw_text(f"time: {round(time, 6)}", -1.6, 0.6, 32)
        draw_text(f"FPS: {round(clock.get_fps(), 1)}", -1.6, 0.5, 32)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)

        pygame.display.flip()
        clock.tick(80)

if __name__ == "__main__":
    main()
