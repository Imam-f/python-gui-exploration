import sys
import sdl2
import sdl2.ext
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Define necessary structs and constants for Windows API interaction
try:
    from sdl2 import SDL_SysWMinfo
except ImportError:
    class SDL_SysWMinfo(ctypes.Structure):
        _fields_ = [("version", sdl2.SDL_version),
                    ("subsystem", ctypes.c_uint32),
                    ("info", ctypes.c_uint64 * 22)]  # This is a simplification

def get_sdl_window_hwnd(sdl_window):
    # Prepare sysWMinfo and obtain window information
    sys_wm_info = SDL_SysWMinfo()
    sdl2.SDL_VERSION(sys_wm_info.version)
    if sdl2.SDL_GetWindowWMInfo(sdl_window, ctypes.byref(sys_wm_info)):
        # Extract the HWND from the info structure
        hwnd = sys_wm_info.info.win.window
        return hwnd
    else:
        return None
    
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Constants for Windows API
WM_SYSCOMMAND = 0x0112
SC_MOVE = 0xF010
HTCAPTION = 0x0002

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

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def drag_window(hwnd):
    """
    Signal Windows to initiate the window drag action.
    """
    user32.ReleaseCapture()
    user32.SendMessageW(hwnd, WM_SYSCOMMAND, SC_MOVE | HTCAPTION, 0)

def run():
    sdl2.ext.init()

    window = sdl2.SDL_CreateWindow(b"SDL2/OpenGL Demo",
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
                                   sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_BORDERLESS)

    if not window:
        print("Could not create window")
        return
    
    # Get the SDL_Window as a ctypes pointer
    sdl_window_ptr = ctypes.cast(window, ctypes.POINTER(sdl2.SDL_Window))
    # Get the native window handle (HWND) using our function
    hwnd = get_sdl_window_hwnd(sdl_window_ptr)
    
    if hwnd:
        # Proceed with modifying the window's attributes for transparency
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x80000
        LWA_COLORKEY = 0x1
        LWA_ALPHA = 0x2

        ctypes.windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE,
                                               ctypes.windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 200, LWA_COLORKEY | LWA_ALPHA)

    context = sdl2.SDL_GL_CreateContext(window)

    # Set OpenGL attributes
    # We want to use OpenGL 3.3 for this example
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)

    # Enable V-Sync
    sdl2.SDL_GL_SetSwapInterval(1)

    running = True
    event = sdl2.SDL_Event()

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    gluPerspective(45, (800/600), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False
            
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                drag_window(hwnd)

        # Clear the screen to a dark blue color
        # glClearColor(0.1, 0.2, 0.3, 0)
        glClearColor(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glRotatef(1, 3, 1, 1)
        Cube()

        # Swap the window buffers
        sdl2.SDL_GL_SwapWindow(window)

    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_GL_DeleteContext(context)
    sdl2.ext.quit()

if __name__ == "__main__":
    run()
