from PIL import ImageFont
import os

fonts_folder = r"C:/Windows/Fonts"  # For Windows
font_files = os.listdir(fonts_folder)

print("Available Fonts:")
for font in font_files:
    if font.lower().endswith(".ttf"):
        print(font)
