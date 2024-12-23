import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

# Initialise Pygame
pygame.init()

# Set up Pygame window
window_width = 800
window_height = 600
display = (window_width, window_height)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Initialise OpenGL
# gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
# glMatrixMode(GL_PROJECTION)
glLoadIdentity()
# glOrtho(0, window_width, 0, window_height, 0.1, 50.0)
# glOrtho(-2, 2, -1.5, 1.5, -1, 50.0)
glOrtho(-4/3, 4/3, -1, 1, -1, 50.0)
glTranslatef(0.0, 0.0, -10)
# glTranslatef(0.0, 0.0, -4)

# Enable texture mapping
glEnable(GL_TEXTURE_2D)
glEnable(GL_DEPTH_TEST)
glClearColor(0.1, 0.1, 0.1, 0)

# Load and set up texture
texture = glGenTextures(1)
image = pygame.image.load('firefly.jpg')
# image = pygame.image.load('asta.jpg')
# image = pygame.image.load('seren.png')
img_data = pygame.image.tostring(image, 'RGB', 1)
width, height = image.get_width(), image.get_height()

glActiveTexture(GL_TEXTURE0)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

# glGenerateMipmap(GL_TEXTURE_2D)

i = 0

# Main rendering loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            # # Read the pixel at position (x, y)
            # glReadBuffer(GL_FRONT)
            # pixels = glReadPixels(0, 0, window_width, window_height, GL_RGB, GL_UNSIGNED_BYTE)

            # import pygame.image

            # # Save pixel data to JPEG using Pygame
            # image = pygame.image.fromstring(pixels, (window_width, window_height), 'RGB')
            # image = pygame.transform.flip(image, False, True) # Flip the image vertically
            # pygame.image.save(image, 'output.jpg')

            # print(pixels)

            pygame.quit()
            quit()

    # glViewport(0, 0, window_width, window_height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Apply rotation to the texture coordinates
    glMatrixMode(GL_TEXTURE)
    glPushMatrix()
    i += 1
    i = i % 360
    glTranslatef(0.5, 0.5, 0)
    glRotatef(i, 0, 0, 1)  # Rotate 45 degrees around the z-axis
    glTranslatef(-0.5, -0.5, 0)

    # glRotatef(1, 3, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord3f(0, 0, 0)
    glVertex3f(-1, -1, 1)

    glTexCoord3f(1, 0, 0)
    glVertex3f(1, -1, 1)

    glTexCoord3f(1, 1, 0)
    glVertex3f(1, 1, 1)

    glTexCoord3f(0, 1, 0)
    glVertex3f(-1, 1, 1)

    glEnd()

    glPopMatrix()
    glFlush()

    # glBegin(GL_QUADS)
    # for surface in surfaces:
    #     x = 0
    #     for vertex in surface:
    #         x+=1
    #         gl.glColor3fv(colors[x])
    #         glVertex3fv(verticies[vertex])
    # glEnd()

    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex in edge:
    #         glVertex3fv(verticies[vertex])
    # glEnd()

    pygame.display.flip()
    pygame.time.wait(10)
