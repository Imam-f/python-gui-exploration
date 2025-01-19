import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class TransparentLogoWindow:
    def __init__(self, image_path):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("")
        
        # Make the window frameless
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # Load the image and keep transparency
        image = Image.open(image_path)
        image = image.convert('RGBA')
        
        # Convert image to numpy array to handle alpha
        data = np.array(image)
        mask = Image.fromarray(data[:, :, 3])  # Extract alpha channel
        
        # Create a fully transparent image for the background
        background = Image.new('RGBA', image.size, (0, 0, 0, 0))
        
        # Composite the image with transparency
        final_image = Image.composite(image, background, mask)
        
        # Convert to PhotoImage for Tkinter
        self.photo = ImageTk.PhotoImage(final_image)
        
        # Create transparent window
        self.root.attributes('-alpha', 0.0)  # Start fully transparent
        self.root.config(bg='white')  # Black background works better for transparency
        
        # Create label with transparent background
        self.label = tk.Label(self.root, image=self.photo, bg='white')
        self.label.pack()
        
        # Center the window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - image.width) // 2
        y = (screen_height - image.height) // 2
        self.root.geometry(f'+{x}+{y}')
        
        # Bind click event to close window
        self.root.bind('<Button-1>', lambda e: self.root.quit())
        
        # Fade in effect
        self.fade_in()
    
    def fade_in(self):
        """Gradually fade in the window"""
        alpha = self.root.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.1
            self.root.attributes('-alpha', alpha)
            self.root.after(50, self.fade_in)

    def show(self):
        self.root.mainloop()

# Example usage
if __name__ == "__main__":
    # Replace 'logo.png' with your PNG file path
    logo_window = TransparentLogoWindow('box.png')
    logo_window.show()