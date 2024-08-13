# tinter

Tint textures with a specified color

# Usage

    Run `python tinter.py --help` to view the command line help:

    usage: Tinter [-h] [-b BASE] [-i INPUT [INPUT ...]] [-o OUTPUT] -c COLOR [COLOR ...]

    Tint textures with a specified color

    options:
      -h, --help            show this help message and exit
      -b BASE, --base BASE  Folder path (for multiple files)
      -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                            File pat(s)
      -o OUTPUT, --output OUTPUT
                            Output path (default ./output)
      -c COLOR [COLOR ...], --color COLOR [COLOR ...]
                            Color value(s) (hex)

# Input files

You can specify the input as a list of filenames:

    $ python tinter.py texture1.png texture2.png texture3.png

Or you can specify a base path for the files:

    $ python tinter.py texture1.png texture2.png texture3.png -b path/to/directory

Or you can specify an entire directory of textures to tint:

    $ python tinter.py -b /path/to/directory
