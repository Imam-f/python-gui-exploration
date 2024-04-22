import tkinter as tk
from PIL import Image, ImageTk
import ctypes

def transparent_window(window, image_path):
    # Load the image using PIL
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    window.image = tk.PhotoImage(file='shovel.png')

    # Set the window size to the image size
    window.geometry(f"{image.width}x{image.height}+200+200")
    window.overrideredirect(True)  # Remove window decorations

    # Create a label for displaying the image
    # label = tk.Label(window, image=photo)
    label = tk.Label(root, image=root.image, bg='white')
    # label.image = photo  # Keep a reference
    label.pack()

    # Make the window background transparent
    window.attributes('-transparentcolor', 'white')

    # Using Windows API to enable transparency (layered window)
    # hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    # extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
    # ctypes.windll.user32.SetWindowLongW(hwnd, -20, extended_style | 0x00080000)
    # ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0x00FFFFFF, 100, 0x00000002)
    # ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 0, 0x00000002)

# Create the main window
root = tk.Tk()

# Call the function to create a transparent window
transparent_window(root, 'shovel.png')

# Display the splash screen for 5 seconds then destroy
root.after(5000, root.destroy)

# Run the application
root.mainloop()
