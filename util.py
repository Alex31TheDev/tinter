from os import path, listdir
import re

from PIL import ImageColor

color_regex = "^#?([a-fA-F0-9]{6})$"

def get_files(dir_path):
    files = [f for f in listdir(dir_path) if path.isfile(path.join(dir_path, f))]
    return files

def parse_color(color_str):
    color_match = re.match(color_regex, color_str)

    if color_match is None:
        return None
    
    color_hex = "#" + color_match.group(1)
    parsed = ImageColor.getcolor(color_hex, "RGB")

    color = (parsed[0] / 255, parsed[1] / 255, parsed[2] / 255)
    return color