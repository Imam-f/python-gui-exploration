import glfw
import OpenGL.GL as gl
import imgui
import platform
from imgui.integrations.glfw import GlfwRenderer

# Platform-specific imports
if platform.system() == "Windows":
    import ctypes
    import ctypes.wintypes

class ClickThroughWindow:
    def __init__(self):
        self.window = None
        self.impl = None
        self.setup_window()
        self.setup_imgui()
        self.setup_click_through()

    def setup_window(self):
        if not glfw.init():
            raise RuntimeError("GLFW initialization failed")

        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
        glfw.window_hint(glfw.DECORATED, glfw.FALSE)
        glfw.window_hint(glfw.FLOATING, glfw.TRUE)
        glfw.window_hint(glfw.ALPHA_BITS, 8)
        
        self.window = glfw.create_window(800, 600, "Click-Through GUI", None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Enable vsync

    def setup_imgui(self):
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)
        
        # Configure OpenGL blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)

        # Configure ImGui style
        style = imgui.get_style()
        style.alpha = 0.7
        style.window_rounding = 5.0
        colors = style.colors
        colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.08, 0.08, 0.08, 0.90)

    def setup_click_through(self):
        """Platform-specific click-through setup"""
        if platform.system() == "Windows":
            hwnd = glfw.get_win32_window(self.window)
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE
            ex_style |= 0x00080000  # WS_EX_LAYERED
            ex_style |= 0x00000020  # WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, -20, ex_style)
            
        elif platform.system() == "Linux":
            from Xlib import display, X
            from Xlib.ext import shape
            
            d = display.Display()
            x11_window = d.create_resource_object(
                'window', 
                glfw.get_x11_window(self.window))
            
            # Create empty input shape region
            region = X.CreateRegion()
            x11_window.shape_input_region(region, shape.SHAPE_INPUT)
            d.flush()

    def update_click_through(self):
        """Optional: Dynamic click-through based on mouse position"""
        io = imgui.get_io()
        if platform.system() == "Windows" and not io.want_capture_mouse:
            # Only allow click-through when not hovering over UI
            hwnd = glfw.get_win32_window(self.window)
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            if not (ex_style & 0x00000020):
                ctypes.windll.user32.SetWindowLongW(hwnd, -20, ex_style | 0x00000020)
        elif platform.system() == "Windows":
            hwnd = glfw.get_win32_window(self.window)
            ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
            if ex_style & 0x00000020:
                ctypes.windll.user32.SetWindowLongW(hwnd, -20, ex_style & ~0x00000020)

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            
            # Start new frame
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            imgui.new_frame()

            # Create demo UI
            imgui.begin("Click-Through Demo", True, 
                        flags=imgui.WINDOW_NO_TITLE_BAR | 
                              imgui.WINDOW_ALWAYS_AUTO_RESIZE)
            imgui.text("Transparent Click-Through GUI")
            imgui.button("Interactive Button")
            imgui.end()

            # Optional dynamic click-through update
            # self.update_click_through()

            # Render
            imgui.render()
            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()

if __name__ == "__main__":
    ClickThroughWindow().run()