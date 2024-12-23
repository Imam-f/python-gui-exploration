from sys import platform
import tkinter as tk
root = tk.Tk()

if platform == "linux" or platform == "linux2":
    root.overrideredirect(True)
    root.wait_visibility(root)
    root.wm_attributes("-alpha", 0.5)
elif platform == "darwin":
    root.overrideredirect(True)
    # Make the root window always on top
    root.wm_attributes("-topmost", True)
    # Turn off the window shadow
    root.wm_attributes("-transparent", True)
    # Set the root window background color to a transparent color
    root.config(bg='systemTransparent')
    root.geometry("+300+300")
    # Store the PhotoImage to prevent early garbage collection
    root.image = tk.PhotoImage(file="shovel.png")
    # Display the image on a label
    label = tk.Label(root, image=root.image)
    # Set the label background color to a transparent color
    label.config(bg='systemTransparent')
    label.pack()
elif platform == "win32":
    root.image = tk.PhotoImage(file='shovel.png')
    label = tk.Label(root, image=root.image, bg='white')
    root.overrideredirect(True)
    root.geometry("+250+250")
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")
    label.pack()

root.mainloop()