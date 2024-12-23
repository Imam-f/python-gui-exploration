import pygetwindow as gw
import pyautogui
import numpy as np
import cv2

def get_window_rect(title):
    win = gw.getWindowsWithTitle(title)[0]
    return win.left, win.top, win.width, win.height

def capture_region(x, y, width, height):
    image = pyautogui.screenshot(region=(x, y, width, height))
    return np.array(image)

def main():
    # Assuming you know the window titles or part of them
    your_window_title = "Untitled - Notepad"
    obscured_window_title = "This PC"

    x1, y1, w1, h1 = get_window_rect(your_window_title)
    x2, y2, w2, h2 = get_window_rect(obscured_window_title)

    # Calculate intersection
    left = max(x1, x2)
    right = min(x1 + w1, x2 + w2)
    top = max(y1, y2)
    bottom = min(y1 + h1, y2 + h2)

    if right > left and bottom > top:
        img = capture_region(left, top, right - left, bottom - top)
        cv2.imshow("Captured Region", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
