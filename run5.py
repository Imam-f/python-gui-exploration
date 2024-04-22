import pygame
from pygame.locals import *
from OpenGL.GL import *
import ctypes
import ctypes.wintypes as w

user32 = ctypes.WinDLL('user32', use_last_error=True)
dwmapi = ctypes.WinDLL('dwmapi', use_last_error=True)

# Constants for Windows API
WM_SYSCOMMAND = 0x0112
SC_MOVE = 0xF010
HTCAPTION = 0x0002

# Constants for Windows API
GWL_STYLE = -16
WS_POPUP = 0x80000000
WS_VISIBLE = 0x10000000
WS_THICKFRAME = 0x00040000

# Define constants
WM_SIZE = 0x0005
GWL_WNDPROC = -4
RDW_INVALIDATE = 0x0001
RDW_ERASE = 0x0004
LRESULT = LONG_PTR = w.LPARAM

# Import the function from user32.dll
SetWindowLongPtr = user32.SetWindowLongPtrA
GetWindowLongPtr = user32.GetWindowLongPtrA
CallWindowProc = user32.CallWindowProcA
GetForegroundWindow = user32.GetForegroundWindow
RedrawWindow = user32.RedrawWindow

# Define the custom window procedure callback type
# WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.wintypes.UINT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)
WNDPROC = ctypes.WINFUNCTYPE(LRESULT, w.HWND, w.UINT, w.WPARAM, w.LPARAM)

user32.GetWindowLongPtrA.argtypes = w.HWND, ctypes.c_int
user32.GetWindowLongPtrA.restype = LONG_PTR
user32.GetForegroundWindow.argtypes = ()
user32.GetForegroundWindow.restype = w.HWND
user32.RedrawWindow.argtypes = w.HWND, w.LPRECT, w.HRGN, w.UINT
user32.RedrawWindow.restype = w.BOOL
user32.CallWindowProcA.argtypes = WNDPROC, w.HWND, w.UINT, w.WPARAM, w.LPARAM
user32.CallWindowProcA.restype = LRESULT
user32.SetWindowLongPtrA.argtypes = w.HWND, ctypes.c_int, LONG_PTR
user32.SetWindowLongPtrA.restype = LONG_PTR

SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
# SetWindowAttribute = user32.SetWindowAttribute
DwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute


def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader

def drag_window():
    """
    Signal Windows to initiate the window drag action.
    """
    hwnd = pygame.display.get_wm_info()["window"]
    user32.ReleaseCapture()
    user32.SendMessageW(hwnd, WM_SYSCOMMAND, SC_MOVE | HTCAPTION, 0)

def main():
    pygame.init()
    display = (800, 600)
    # screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL|RESIZABLE)
    screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL|NOFRAME|RESIZABLE)
    
    hwnd = pygame.display.get_wm_info()["window"]

    # Get the current window style
    current_style = user32.GetWindowLongW(hwnd, GWL_STYLE)

    # Modify the window style to be borderless but still resizable
    # This removes the title bar and edges but allows resizing
    new_style = WS_POPUP | WS_VISIBLE | WS_THICKFRAME
    user32.SetWindowLongW(hwnd, GWL_STYLE, new_style)

    glViewport(0, 0, display[0], display[1])
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Shader Program
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec4 color;
    out vec4 vertexColor;
    void main()
    {
        gl_Position = vec4(position, 1.0);
        vertexColor = color;
    }
    """
    fragment_shader = """
    #version 330
    in vec4 vertexColor;
    out vec4 fragColor;
    void main()
    {
        fragColor = vertexColor;
    }
    """
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, create_shader(GL_VERTEX_SHADER, vertex_shader))
    glAttachShader(shaderProgram, create_shader(GL_FRAGMENT_SHADER, fragment_shader))
    glLinkProgram(shaderProgram)
    glUseProgram(shaderProgram)

    # Vertex Input
    vertices = [
        -0.5, -0.5, 0.0,  1.0, 0.0, 0.0, 1.0,  # Red, fully opaque
         0.5, -0.5, 0.0,  0.0, 0.5, 0.0, 0.1,  # Green, fully opaque
         0.0,  0.5, 0.0,  0.0, 0.0, 1.0, 0.5   # Blue, fully opaque
    ]
    vertices = (GLfloat * len(vertices))(*vertices)

    # VAO and VBO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW)

    # Position Attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 7 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # Color Attribute
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 7 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)

    # Make the window transparent
    hwnd = pygame.display.get_wm_info()["window"]
    ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, ctypes.windll.user32.GetWindowLongPtrW(hwnd, -20) | 0x80000)
    # ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 230, 0x3)  # Making black color transparent
    # ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0xFFFFFF, 240, 0x1)  # Making black color transparent
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 0, 0x1)  # Making black color transparent
    # ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 220, 0x2)  # Making black color transparent

    # ctypes.windll.user32.WINDOWCOMPOSITIONATTRIBDATA


    class ACCENTPOLICY(ctypes.Structure):
        _fields_ = [
            ("na", ctypes.c_int),
            ("nf", ctypes.c_int),
            ("nc", ctypes.c_int),
            ("nA", ctypes.c_int),
        ]

    class WINCOMPATTRIBDATA(ctypes.Structure):
        _fields_ = [
            ("na", ctypes.c_int),
            ("PD", ctypes.c_void_p),
            ("ULONG", ctypes.c_ulong),
        ]

    # policy = ACCENTPOLICY(2, 0xFFFFFF, 0x0000FF, 1)
    policy = ACCENTPOLICY(3, 0, 0, 0)
    print(ctypes.sizeof(ACCENTPOLICY))
    data = WINCOMPATTRIBDATA(19, ctypes.cast(ctypes.byref(policy), ctypes.c_void_p), ctypes.sizeof(ACCENTPOLICY))
    # SetWindowCompositionAttribute(hwnd, ctypes.byref(data))
    
    # Rounded
    # preference = ctypes.c_int(3)
    preference = ctypes.c_int(2)
    # DwmSetWindowAttribute(hwnd, 33, ctypes.byref(preference), 4)

    # Enable mica
    preference_2 = ctypes.c_int(1)
    DwmSetWindowAttribute(hwnd, 1029, ctypes.byref(preference_2), 4)

    # Dark mode
    preference_3 = ctypes.c_int(1)
    DwmSetWindowAttribute(hwnd, 20, ctypes.byref(preference_3), 4)

    # Backdrop
    #         /// no backdrop
    #         DWMSBT_NONE = 1,
    #         /// Use tinted blurred wallpaper backdrop (Mica)
    #         DWMSBT_MAINWINDOW = 2,
    #         /// Use Acrylic backdrop
    #         DWMSBT_TRANSIENTWINDOW = 3,
    #         /// Use blurred wallpaper backdrop
    #         DWMSBT_TABBEDWINDOW = 4
    
    preference_3 = ctypes.c_int(2)
    DwmSetWindowAttribute(hwnd, 38, ctypes.byref(preference_3), 4)

    def draw_game() -> None:
        # print("B")
        # glClearColor(1.0, 1.0, 1.0, 0.5)  # Set the background color to black and fully transparent
        # glClearColor(0, 0, 0, 1)  # Set the background color to black and fully transparent
        # glClearColor(0.1, 0.1, 0.1, 0.5)  # Set the background color to black and fully transparent
        glClearColor(0, 0, 0, 0)  # Set the background color to black and fully transparent
        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        pygame.display.flip()

    hWnd = GetForegroundWindow()
    originalWndProcPtr = GetWindowLongPtr(hWnd, GWL_WNDPROC)

    def wndProc(hWnd, message, wParam, lParam):
        if message == WM_SIZE:
            draw_game()
            # Call RedrawWindow to redraw the entire window
            RedrawWindow(hWnd, None, None, RDW_INVALIDATE | RDW_ERASE)
        # return CallWindowProc(ctypes.c_void_p(originalWndProcPtr), hWnd, message, wParam, lParam)
        return CallWindowProc(ctypes.cast(originalWndProcPtr, WNDPROC), hWnd, message, wParam, lParam)

    # Wrap wndProc with WNDPROC type and store the original window procedure pointer
    print("a")

    SetWindowLongPtr(hWnd, GWL_WNDPROC, ctypes.cast(WNDPROC(wndProc), ctypes.c_void_p).value)
    # SetWindowLongPtr(hWnd, GWL_WNDPROC, WNDP/ROC(wndProc))
    # originalWndProcPtr = SetWindowLongPtr(hwnd, GWL_WNDPROC, WNDPROC(lambda *args: wndProc(originalWndProcPtr, draw_game, *args)))
    print("b")

    resizing = False
    mouse_pos = pygame.mouse.get_pos()
    print("c")

    while True:
        for event in pygame.event.get():
            # print("c")

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Assuming the title bar is at the top of the window with a height of 50 pixels
                if event.pos[1] < display[1]//2:
                    drag_window()
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    display_init = display
                    resizing = True
                    
            if event.type == pygame.MOUSEBUTTONUP:
                try:
                    display = display_temp
                except:
                    display = display
                resizing = False

            if event.type == pygame.VIDEORESIZE:
                # pygame.display.set_mode((event.w, event.h), DOUBLEBUF|OPENGL|RESIZABLE)
                pygame.display.set_mode((event.w, event.h), DOUBLEBUF|OPENGL|NOFRAME|RESIZABLE)
                glViewport(0, 0, event.w, event.h)
                draw_game()

        if resizing:
            display_temp = (
                        display_init[0] - mouse_pos[0] + pygame.mouse.get_pos()[0], 
                        display_init[1] - mouse_pos[1] + pygame.mouse.get_pos()[1]
                    )
            print(display_temp)
            # screen = pygame.display.set_mode(display_temp, DOUBLEBUF|OPENGL|RESIZABLE)
            old_surface_saved = screen.copy()
            screen = pygame.display.set_mode(display_temp, DOUBLEBUF|OPENGL|NOFRAME|RESIZABLE)
            screen.blit(old_surface_saved, (0, 0))
            del old_surface_saved
            glViewport(0, 0, display_temp[0], display_temp[1])
        
        draw_game()
        # pygame.time.wait(10)
        # if not resizing:
        #     pygame.display.flip()


if __name__ == "__main__":
    main()
