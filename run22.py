import pygetwindow as gw
import pyautogui
import numpy as np
from PIL import Image

def capture_entire_screen():
    return pyautogui.screenshot()

def get_window_area(window_title):
    win = gw.getWindowsWithTitle(window_title)[0]
    return win.left, win.top, win.width, win.height

def mask_out_window(screen_image, x, y, width, height):
    # Convert screenshot to numpy array for manipulation
    screen_np = np.array(screen_image)
    screen_np[y:y+height, x:x+width] = 0  # Set the window area to black or any color that indicates masking
    return Image.fromarray(screen_np)

def main():
    screen = capture_entire_screen()
    x, y, width, height = get_window_area("This PC")  # Specify the title of the window
    obscured_desktop = mask_out_window(screen, x, y, width, height)
    obscured_desktop.show()

if __name__ == "__main__":
    main()
