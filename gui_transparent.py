import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer

def main():
    # Initialize GLFW with transparency hints
    if not glfw.init():
        print("Could not initialize GLFW")
        return

    # Configure window hints for transparency
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)  # Optional: remove window decorations
    glfw.window_hint(glfw.ALPHA_BITS, 8)

    # Create window with transparent background
    window = glfw.create_window(1280, 720, "Transparent PyImgui", None, None)
    if not window:
        glfw.terminate()
        print("Could not create GLFW window")
        return

    glfw.make_context_current(window)

    # Initialize ImGui
    imgui.create_context()
    impl = GlfwRenderer(window)

    # Enable OpenGL blending for transparency
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)  # Transparent clear color

    # Configure ImGui style with transparency
    style = imgui.get_style()
    style.alpha = 0.8  # Overall transparency factor
    style.window_rounding = 5.0

    # Custom colors with alpha channel
    colors = style.colors
    colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.08, 0.08, 0.08, 0.90)
    colors[imgui.COLOR_FRAME_BACKGROUND] = (0.20, 0.20, 0.20, 0.50)
    colors[imgui.COLOR_BUTTON] = (0.25, 0.25, 0.25, 0.40)

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        # Clear with transparent color
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Start new ImGui frame
        imgui.new_frame()

        # Create a semi-transparent window
        imgui.begin("Transparent Window", True, 
                    flags=imgui.WINDOW_NO_TITLE_BAR | 
                          imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        
        imgui.text("This is transparent GUI!")
        imgui.text_colored("Colored text with alpha", 1.0, 0.5, 0.0, 0.8)
        imgui.button("Semi-transparent button")
        imgui.end()

        # Render ImGui
        imgui.render()
        impl.render(imgui.get_draw_data())

        # Swap buffers
        glfw.swap_buffers(window)

    # Cleanup
    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()