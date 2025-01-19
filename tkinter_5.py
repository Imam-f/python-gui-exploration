import tkinter as tk
from PIL import Image, ImageTk
import time

class TransparentSplashScreen:
    def __init__(self, image_path=None, duration=3):
        self.duration = duration
        
        # Create the main window
        self.root = tk.Tk()
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Set transparency
        self.root.attributes('-alpha', 0.7)  # 0.0 is fully transparent, 1.0 is opaque
        
        # Make background transparent
        # self.root.config(bg='systemTransparent')  # For MacOS
        self.root.attributes('-transparentcolor', 'systemTransparent')  # For Windows
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size (adjust as needed)
        window_width = 400
        window_height = 300
        
        # Calculate center position
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Position window in center
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create label for content
        self.label = tk.Label(
            self.root,
            text="Loading...",
            font=("Arial", 24),
            bg='systemTransparent',
            fg='white'
        )
        
        # If image path is provided, load and display image
        if image_path:
            try:
                # Load and resize image
                image = Image.open(image_path)
                image = image.resize((window_width, window_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Update label with image
                self.label.configure(image=photo)
                self.label.image = photo  # Keep a reference
            except Exception as e:
                print(f"Error loading image: {e}")
        
        self.label.pack(expand=True)
        
        # Bind mouse click to close window
        self.root.bind('<Button-1>', lambda e: self.close())
        
    def show(self):
        """Display the splash screen"""
        # Schedule closing after duration
        self.root.after(int(self.duration * 1000), self.close)
        self.root.mainloop()
        
    def close(self):
        """Close the splash screen"""
        self.root.destroy()

# Example usage
if __name__ == "__main__":
    # Create and show splash screen
    splash = TransparentSplashScreen(duration=3, image_path='box.png')  # Shows for 3 seconds
    splash.show()
    
    # Your main application code would go here
    print("Main application starting...")