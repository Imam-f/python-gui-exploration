import tkinter as tk
from tkinter import ttk

class FloatingSidebarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop App with Floating Sidebar")
        self.root.geometry("800x600")

        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar frame
        self.sidebar = tk.Frame(self.root, bg="#333", width=600, height=600)
        self.sidebar.place(x=0, y=0)

        # Toggle button
        self.toggle_button = ttk.Button(self.root, text="Toggle Sidebar", command=self.toggle_sidebar)
        self.toggle_button.place(x=10, y=10)

        # Content in the main area
        self.content_label = ttk.Label(self.main_frame, anchor="center", text="Main Content Area", font=("Arial", 16))
        self.content_label.pack(expand=True, fill="both")

        # Initial state of sidebar
        self.sidebar_visible = True

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.place_forget()
        else:
            self.sidebar.place(x=0, y=0)
        self.sidebar_visible = not self.sidebar_visible

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingSidebarApp(root)
    root.mainloop()
