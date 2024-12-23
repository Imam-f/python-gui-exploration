import ctypes as ct
from ctypes import wintypes as w

import pygame

# LPARAM is typedef'ed as LONG_PTR in winuser.h, so it can be used
# for LRESULT and LONG_PTR which are missing from wintypes.
LRESULT = LONG_PTR = w.LPARAM
WNDPROC = ct.WINFUNCTYPE(LRESULT, w.HWND, w.UINT, w.WPARAM, w.LPARAM)
WM_SIZE = 0x0005
RDW_INVALIDATE = 0x0001
RDW_ERASE = 0x0004
GWL_WNDPROC = -4

# ctypes.windll.user32 is a cached, shared version of user32.dll.
# Get our own copy and meticulously define argtypes/restype according
# to MSDN documentation of the C prototypes.
user32 = ct.WinDLL('user32')
user32.GetWindowLongPtrA.argtypes = w.HWND, ct.c_int
user32.GetWindowLongPtrA.restype = LONG_PTR
user32.GetForegroundWindow.argtypes = ()
user32.GetForegroundWindow.restype = w.HWND
user32.RedrawWindow.argtypes = w.HWND, w.LPRECT, w.HRGN, w.UINT
user32.RedrawWindow.restype = w.BOOL
user32.CallWindowProcA.argtypes = WNDPROC, w.HWND, w.UINT, w.WPARAM, w.LPARAM
user32.CallWindowProcA.restype = LRESULT
user32.SetWindowLongPtrA.argtypes = w.HWND, ct.c_int, LONG_PTR
user32.SetWindowLongPtrA.restype = LONG_PTR

def main():
    pygame.init()

    screen = pygame.display.set_mode((320, 240), pygame.RESIZABLE | pygame.DOUBLEBUF)

    def draw_game():
        screen.fill(pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color('red'), pygame.Rect(0,0,screen.get_width(),screen.get_height()).inflate(-10, -10))
        pygame.display.flip()
    
    old_window_proc = user32.GetWindowLongPtrA(user32.GetForegroundWindow(), GWL_WNDPROC)

    def new_window_proc(hwnd, msg, wparam, lparam):
        if msg == WM_SIZE:
            draw_game()
            user32.RedrawWindow(hwnd, None, None, RDW_INVALIDATE | RDW_ERASE)
        # LONG_PTR is the same bit width as WNDPROC, but
        # need cast to use it here.
        return user32.CallWindowProcA(ct.cast(old_window_proc, WNDPROC), hwnd, msg, wparam, lparam)

    new_window_proc_cb = WNDPROC(new_window_proc)

    # Can't cast a WNDPROC (pointer) to a LONG_PTR directly, but can cast to void*.
    # The .value of a c_void_p instance is its integer address.
    user32.SetWindowLongPtrA(user32.GetForegroundWindow(), GWL_WNDPROC, ct.cast(new_window_proc_cb, ct.c_void_p).value)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE| pygame.DOUBLEBUF)
        draw_game()
        
if __name__ == '__main__':
    main()