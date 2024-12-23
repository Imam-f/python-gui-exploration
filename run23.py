import pygetwindow as gw
import pyautogui
import time

def capture_screen():
    return pyautogui.screenshot()

def main():
    window_title = "Home"  # Replace with the actual title of your window
    win = gw.getWindowsWithTitle(window_title)[0]

    if win:
        win.minimize()  # Minimize or hide the window
        time.sleep(1)  # Wait a moment for the window to minimize

        screen = capture_screen()
        screen.show()

        win.maximize()  # Restore the window
        time.sleep(1)  # Wait a moment for the window to restore

if __name__ == "__main__":
    main()
