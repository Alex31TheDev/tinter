import argparse
import sys

from os import path, makedirs
from PIL import Image, UnidentifiedImageError

from util import get_files, parse_color
from blend_modes import blend_modes

image_mode = "RGBA"

def tint_image(image, colors, blend_mode=0):
    width, height = image.size
    pixels = image.load()

    has_alpha = image.mode == "RGBA"
    blend_func = blend_modes[blend_mode]

    if blend_func is None:
        raise Exception("Invalid blend mode")

    color_count = len(colors)
    images = [Image.new(image_mode, image.size) for i in range(color_count)]

    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]

            for i, color in enumerate(colors):
                tinted = blend_func(pixel, color)

                if has_alpha:
                    tinted += (pixel[3],)

                images[i].putpixel((x, y), tinted)

    return images

def parse_paths(input_paths, base_path):
    if base_path is not None:
        base_path = path.abspath(base_path)

    if base_path is None:
        paths = input_paths
    elif input_paths is None:
        paths = get_files(base_path)
        paths = [path.join(base_path, x) for x in paths]
    else:
        paths = [path.join(base_path, x) for x in input_paths]

    return paths

def parse_colors(color_strs):
    colors, colors_ok = [], True

    for color_str in color_strs:
        color = parse_color(color_str)

        if color is None:
            print("Error: Invalid color:", color_str)
            colors_ok = False
        else:
            colors.append(color)

    return colors, colors_ok

def load_images(paths):
    images = []

    for img_path in paths:
        try:
            image = Image.open(img_path, "r")

            if not image.mode in ["RGB", "RGBA"]:
                image = image.convert("RGB")

            images.append(image)
        except FileNotFoundError:
            print(f"Error: Texture \"{img_path}\" wasn't found.")
        except UnidentifiedImageError:
            print(f"Error: Texture \"{img_path}\" is invalid.")

    return images

def tint_and_save_images(images, colors, paths, output):
    output = path.abspath(output)

    for i, image in enumerate(images):
        name, ext = path.splitext(paths[i])

        try:
            name = path.basename(name)
        except:
            pass

        tinted_images = tint_image(image, colors)
        image.close()

        multiple_images = len(tinted_images) > 1

        for i, tinted_image in enumerate(tinted_images):
            num = ("_" + str(i + 1)) if multiple_images else ""
            img_path = path.join(output, f"{name}{num}{ext}")

            tinted_image.save(img_path)
            print("Saved:", img_path)

usage = "Run python tinter.py --help for usage."

def main():
    parser = argparse.ArgumentParser(
        prog="Tinter", description="Tint textures with a specified color")
    parser.add_argument("-b", "--base",
                        help="Folder path (for multiple files)")
    parser.add_argument("-i", "--input", nargs="+",
                        help="File path(s)")
    parser.add_argument("-o", "--output", default="./output",
                        help="Output path")
    parser.add_argument("-c", "--color", required=True, nargs='+',
                        help="Color value(s) (hex)")

    if len(sys.argv) < 2:
        parser.print_help()
        return

    args = parser.parse_args()
    paths = parse_paths(args.input, args.base)

    if args.output != "." and not path.exists(args.output):
        makedirs(args.output)

    colors, colorsOk = parse_colors(args.color)

    if not colorsOk:
        print("\nAll colors must be hex.\n" + usage)
        return

    images = load_images(paths)
    tint_and_save_images(images, colors, paths, args.output)

if __name__ == "__main__":
    main()
