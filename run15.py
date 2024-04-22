import tkinter as tk

root = tk.Tk()
# Hide the root window drag bar and close button
root.overrideredirect(True)
# Make the root window always on top
root.wm_attributes("-topmost", True)
# Turn off the window shadow
root.wm_attributes("-transparent", 1)
# Set the root window background color to a transparent color
root.config(bg='systemTransparent')

root.geometry("+300+300")

# Store the PhotoImage to prevent early garbage collection
root.image = tk.PhotoImage(file='shovel.png')
# Display the image on a label
label = tk.Label(root, image=root.image)
# Set the label background color to a transparent color
label.config(bg='systemTransparent')
label.pack()

root.mainloop()