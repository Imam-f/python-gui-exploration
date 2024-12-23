import pygame
import ctypes
import sys
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

# Initialize SDL2 and create a window
pygame.init()
window = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF | pygame.NOFRAME | pygame.RESIZABLE)
pygame.display.set_caption("Draggable Window")

# OpenGL settings for transparency
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Constants for Windows API
WM_SYSCOMMAND = 0x0112
SC_MOVE = 0xF010
HTCAPTION = 0x0002

# user32 = ctypes.WinDLL('user32', use_last_error=True)

# # Get the window handle (HWND)
# hwnd = pygame.display.get_wm_info()["window"]

# # Set window style to layered (to allow transparency)
# ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, ctypes.windll.user32.GetWindowLongPtrW(hwnd, -20) | 0x80000)

# # Set the transparency of the window
# # The first parameter is the color to be transparent and the second one is the transparency level
# ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 220, 0x2)  # 220 out of 255 for the transparency level

def drag_window():
    """
    Signal Windows to initiate the window drag action.
    """
    hwnd = pygame.display.get_wm_info()["window"]
    # user32.ReleaseCapture()
    # user32.SendMessageW(hwnd, WM_SYSCOMMAND, SC_MOVE | HTCAPTION, 0)

# Create and compile the vertex shader
vertex_shader_source = """
#version 330 core

layout (location = 0) in vec3 position;

void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
}
"""
vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)

# Create and compile the fragment shader
fragment_shader_source = """
#version 330 core

out vec4 fragColor;

void main()
{
    fragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""
fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)

# Create a shader program and attach the vertex and fragment shaders
shader_program = compileProgram(vertex_shader, fragment_shader)

# Create a vertex buffer object (VBO) and vertex array object (VAO)
vbo = glGenBuffers(1)
vao = glGenVertexArrays(1)

# Bind the VAO
glBindVertexArray(vao)

# Bind the VBO and upload vertex data
glBindBuffer(GL_ARRAY_BUFFER, vbo)
vertices = [
    -0.5, -0.5, 0.0,
    0.5, -0.5, 0.0,
    0.0, 0.5, 0.0
]
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)

# Specify the vertex attribute pointers
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

# Unbind the VAO
glBindVertexArray(0)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Assuming the title bar is at the top of the window with a height of 50 pixels
            if event.pos[1] < 50 or True:
                drag_window()

    # Clear the screen
    glClearColor(0.0, 0.2, 0.8, 0.5)
    glClear(GL_COLOR_BUFFER_BIT)

    # Use the shader program
    glUseProgram(shader_program)

    # Bind the VAO
    glBindVertexArray(vao)

    # Draw the triangles
    glDrawArrays(GL_TRIANGLES, 0, 3)

    # Unbind the VAO
    glBindVertexArray(0)

    # Swap buffers
    pygame.display.flip()

# Cleanup
glDeleteProgram(shader_program)
glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)
glDeleteBuffers(1, [vbo])
glDeleteVertexArrays(1, [vao])
pygame.quit()
