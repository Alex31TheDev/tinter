import argparse
import sys

import re
import math

from os import path, listdir, makedirs
from PIL import Image, ImageColor, UnidentifiedImageError

def blendPixel(pixel, color):
    return (math.floor(pixel[0] * color[0]),
            math.floor(pixel[1] * color[1]),
            math.floor(pixel[2] * color[2]))

def tintImage(image, colors):
    width, height = image.size
    pixels = image.load()

    images = [Image.new("RGB", image.size) for i in range(len(colors))]

    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]

            if len(colors) == 1:
                tinted = blendPixel(pixel, colors[0])
                images[0].putpixel((x, y), tinted)
            else:
                for i, color in enumerate(colors):
                    tinted = blendPixel(pixel, color)
                    images[i].putpixel((x, y), tinted)

    return images

def getFiles(dirPath):
    files = [f for f in listdir(dirPath) if path.isfile(path.join(dirPath, f))]
    return files

usage = "Run python tinter.py --help for usage."

def main():
    parser = argparse.ArgumentParser(prog="Tinter", description="Tint textures with a specified color")
    parser.add_argument("-b", "--base",
                        help="Folder path (for multiple files)")
    parser.add_argument("-i", "--input",nargs="+",
                        help="File path(s)")
    parser.add_argument("-o", "--output", default="./output",
                        help="Output path")
    parser.add_argument("-c", "--color", required=True, nargs='+',
                        help="Color value(s) (hex)")
    
    if len(sys.argv) < 2:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.base is None:
        paths = args.input
    elif args.input is None:
        paths = getFiles(args.base)
    else:
        paths = [path.join(args.base, x) for x in args.input]
    
    if args.output != "." and not path.exists(args.output):
        makedirs(args.output)

    colors, colorsOk = [[], True]

    for color in args.color:
        colorMatch = re.match("^#?([a-fA-F0-9]{6})$", color)

        if colorMatch is None:
            print("Invalid color:", color)
            colorsOk = False
        else:
            parsed = ImageColor.getcolor("#" + colorMatch.group(1), "RGB")
            colors.append((parsed[0] / 255, parsed[1] / 255, parsed[2] / 255))

    if not colorsOk:
        print("\nAll colors must be hex.\n" + usage)
        return
    
    images = []

    for _path in paths:
        try:
            images.append(Image.open(_path, "r"))
        except FileNotFoundError:
            print("Texture", _path, "wasn't found.")
        except UnidentifiedImageError:
            print("Texture", _path, "is invalid.")

    for i, image in enumerate(images):
        name, ext = path.splitext(paths[i])

        try:
            name = path.basename(name)
        except:
            pass
        
        for i, out in enumerate(tintImage(image, colors)):
            _path = path.join(args.output, f"{name}_{i + 1}{ext}")

            out.save(_path)
            print("Saved:", _path)

        image.close()

if __name__ == "__main__":
    main()