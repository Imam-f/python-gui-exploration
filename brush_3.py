import win32gui
import win32con

# Get the device context for the entire screen (desktop)
hDC = win32gui.GetDC(0)

# Create a solid blue brush.
# Note: Colors are specified as 0x00BBGGRR (in hexadecimal).
blue_color = 0x00FF0000  # Red component is 0x00, Green is 0x00, Blue is 0xFF
hBrush = win32gui.CreateSolidBrush(blue_color)

# Create a memory device context compatible with the screen
memDC = win32gui.CreateCompatibleDC(hDC)

# Select the brush into the memory DC
oldBrush = win32gui.SelectObject(memDC, hBrush)

# Define the rectangle coordinates (left, top, right, bottom)
rect = (100, 100, 400, 300)

try:
    while True:
        # Fill the rectangle on the screen's DC using the brush from memDC.
        # (Note: There are several ways to do drawing; this is just one simple example)
        win32gui.FillRect(hDC, rect, hBrush)
except Exception as e:
    # Cleanup: restore the old brush and delete objects
    win32gui.SelectObject(memDC, oldBrush)
    win32gui.DeleteDC(memDC)
    win32gui.DeleteObject(hBrush)
    win32gui.ReleaseDC(0, hDC)
