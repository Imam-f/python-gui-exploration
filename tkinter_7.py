from tkinter import Tk, Label
from PIL import Image, ImageTk
import time

# Create the main window
root = Tk()

# Remove window decorations
root.overrideredirect(True)

# Set window background color (choose a color not present in your image)
root.config(bg='white')

# Make the window transparent by setting the transparent color
root.wm_attributes("-transparentcolor", "white")

# Load the transparent PNG image using Pillow
# image = Image.open("shovel.png")  # Replace with your image path
image = Image.open("box.png")  # Replace with your image path
photo = ImageTk.PhotoImage(image)

# Create a label to display the image with the same background color
label = Label(root, image=photo, bg='white')
label.pack()

# Center the splash screen on the screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')
# root.geometry(f'{width//10}x{height//10}+{100}+{100}')

# Close the splash screen after 3 seconds
root.after(3000, root.destroy)

# Run the application
root.mainloop()