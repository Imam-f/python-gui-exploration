import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Label

class TransparentLogoWindow:
    def __init__(self, image_path):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("")
        
        # Make the window frameless
        self.root.overrideredirect(True)
        
        # Make the window transparent
        self.root.attributes('-alpha', 1.0)
        self.root.attributes('-topmost', True)
        
        # Load and convert the image
        image = Image.open(image_path)
        # Convert RGBA to RGBA to ensure transparency is preserved
        image = image.convert('RGBA')
        
        # Convert PIL image for Tkinter
        self.photo = ImageTk.PhotoImage(image)
        
        # Create label with image
        self.label = Label(self.root, image=self.photo, bg='white')
        self.label.pack()
        
        # Configure the window to be transparent
        self.root.wm_attributes('-transparentcolor', 'white')
        
        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - image.width) // 2
        y = (screen_height - image.height) // 2
        self.root.geometry(f'+{x}+{y}')
        
        # Bind click event to close window
        self.root.bind('<Button-1>', lambda e: self.root.quit())
        
    def show(self):
        self.root.mainloop()

# Example usage
if __name__ == "__main__":
    # Replace 'logo.png' with your PNG file path
    logo_window = TransparentLogoWindow('shovel.png')
    logo_window.show()