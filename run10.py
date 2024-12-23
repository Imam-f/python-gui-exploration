import tkinter as tk

def create_borderless_window():
    # Create a root window
    root = tk.Tk()
    root.overrideredirect(True)  # This removes the border and title bar
    root.geometry("300x200+100+100")  # Set the window size and position

    # Create a frame as the window content
    frame = tk.Frame(root, bg='white')
    frame.pack(fill=tk.BOTH, expand=True)

    # Add a label as an example of content in the frame
    label = tk.Label(frame, text="This is a borderless window", bg='white')
    label.pack(pady=50)

    # Drag functionality
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def stop_move(event):
        root.x = None
        root.y = None

    def do_move(event):
        deltax = event.x - root.x
        deltay = event.y - root.y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")

    # Bind mouse events for dragging the window
    root.bind("<ButtonPress-1>", start_move)
    root.bind("<ButtonRelease-1>", stop_move)
    root.bind("<B1-Motion>", do_move)

    root.mainloop()

create_borderless_window()
