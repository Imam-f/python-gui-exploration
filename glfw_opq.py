import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image  # Pillow library for image loading

def main():
    if not glfw.init():
        return

    # Request a transparent framebuffer
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE) # Remove window decorations


    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    width, height = 800, 600
    window = glfw.create_window(width, height, "Transparent Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Load image with alpha channel
    try:
        image = Image.open("box.png")  # Replace with your image
    except FileNotFoundError:
        print("Error: Image file not found.")
        glfw.terminate()
        return

    image_width, image_height = image.size
    image_data = image.convert("RGBA").tobytes("raw", "RGBA")

    # Create texture
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        image_width,
        image_height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        image_data,
    )

    # Enable blending
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Set up orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)  # Left, Right, Bottom, Top, Near, Far
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    while not glfw.window_should_close(window):
        # Clear the color buffer with a transparent color (RGBA: 0, 0, 0, 0)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw textured quad
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(image_width, 0)
        glTexCoord2f(1, 1)
        glVertex2f(image_width, image_height)
        glTexCoord2f(0, 1)
        glVertex2f(0, image_height)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
