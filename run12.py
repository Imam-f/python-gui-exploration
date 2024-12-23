import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw

def main():
    # Initialize GLFW
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # Create a GLFW window
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 1)

    window = glfw.create_window(1280, 720, "ImGui + GLFW", None, None)
    glfw.make_context_current(window)

    # Initialize ImGui + GLFW
    imgui.create_context()
    impl = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        # Create a detached ImGui window
        imgui.begin("Detached Window", True, imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        imgui.text("This is a simple detached window!")
        imgui.end()

        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()
