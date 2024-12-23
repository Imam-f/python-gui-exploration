import ctypes
import os
from PIL import Image

SPI_GETDESKWALLPAPER = 0x0073
MAX_PATH = 260
path = ctypes.create_unicode_buffer(MAX_PATH)
ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, MAX_PATH, path, 0)

wallpaper_path = path.value
print("Wallpaper path:", wallpaper_path)

# Now you load this image and apply necessary transformations
wallpaper_image = Image.open(wallpaper_path)
# Example transformation: resize to fit a specific resolution
wallpaper_image = wallpaper_image.resize((1920, 1080), Image.ANTIALIAS)
wallpaper_image.save('transformed_wallpaper.png')
