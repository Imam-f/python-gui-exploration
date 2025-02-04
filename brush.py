from Xlib import X, display

# Connect to the X server and get the root window
d = display.Display()
root = d.screen().root

# Create a Graphics Context (GC) with a desired foreground color.
# For example, we use the screen’s white pixel.
gc = root.create_gc(
    foreground=d.screen().white_pixel,
    background=d.screen().black_pixel
)

# Define the rectangle: (x, y, width, height)
x, y, width, height = 100, 100, 300, 200

root.draw_text(gc, 100, 100, b"Hello, world!")  # changed the coords more towards the center

# Draw a rectangle outline (using poly_rectangle)
# Note: poly_rectangle expects a list of rectangles, where each rectangle is a tuple.
rectangles = [(x, y, width, height)]
root.poly_rectangle(gc, rectangles)

# Alternatively, to fill the rectangle, you can use:
root.fill_rectangle(gc, x, y, width, height)

import time
# time.sleep(5)

# Flush the requests to the X server
d.flush()
time.sleep(5)
