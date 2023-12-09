# convert an image into a PNG with unique tiles (squares) only

import os, sys
from collections import OrderedDict
from itertools import chain
try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow module required. See https://python-pillow.org")

# output image settings
BACKGROUND_COLOR = (0xff, 0x00, 0xff)
TILES_PER_ROW = 16

def parse_arguments():
    # parse command line arguments

    if not 3 <= len(sys.argv) <= 5:
        sys.exit(
            "Convert an image into a PNG with distinct tiles only. "
            "Arguments: inputFile outputFile [tileSize [tileOrder]]. "
            "See README.md for more info."
        )

    # files
    (inputFile, outputFile) = sys.argv[1:3]
    if not os.path.isfile(inputFile):
        sys.exit("Input file not found.")
    if os.path.exists(outputFile):
        sys.exit("Output file already exists.")

    # tile size
    tileSize = sys.argv[3] if len(sys.argv) >= 4 else "8"
    try:
        tileSize = int(tileSize)
        if not 4 <= tileSize <= 64:
            raise ValueError
    except ValueError:
        sys.exit("Tile size argument is not valid.")

    # order
    tileOrder = sys.argv[4].upper() if len(sys.argv) >= 5 else "O"
    if tileOrder not in ("O", "P", "A", "C", "CP", "CA"):
        sys.exit("Tile order argument is not valid.")

    return (inputFile, outputFile, tileSize, tileOrder)

def get_unique_tiles(handle, tileSize):
    # tileSize: tile width & height
    # return: list of unique tuples of (red, green, blue) tuples in original
    #         order

    handle.seek(0)
    image = Image.open(handle)

    if image.width == 0 or image.width % tileSize:
        sys.exit("Image width is not valid.")
    if image.height == 0 or image.height % tileSize:
        sys.exit("Image height is not valid.")

    if image.mode in ("L", "P"):
        image = image.convert("RGB")
    elif image.mode != "RGB":
        sys.exit("Unrecognized pixel format (try removing the alpha channel).")

    # TODO: perhaps maintain a separate set to speed up lookup?
    uniqueTiles = []

    for y in range(0, image.height, tileSize):
        for x in range(0, image.width, tileSize):
            tile = tuple(
                image.crop((x, y, x + tileSize, y + tileSize)).getdata()
            )
            if tile not in uniqueTiles:
                uniqueTiles.append(tile)

    return uniqueTiles

def write_image(handle, uniqueTiles, tileSize):
    # write unique tiles to an image;
    # tileSize: tile width & height
    # uniqueTiles: list of tuples of (red, green, blue) tuples

    width = TILES_PER_ROW * tileSize
    # height = ceil(len(uniqueTiles) / TILES_PER_ROW) * tileSize
    height = (len(uniqueTiles) + TILES_PER_ROW - 1) // TILES_PER_ROW * tileSize
    image = Image.new("RGB", (width, height), BACKGROUND_COLOR)

    # copy pixels to image via temporary image
    tileImage = Image.new("RGB", (tileSize, tileSize))
    for (i, tile) in enumerate(uniqueTiles):
        (y, x) = divmod(i, TILES_PER_ROW)
        tileImage.putdata(tile)
        image.paste(tileImage, (x * tileSize, y * tileSize))

    handle.seek(0)
    image.save(handle, "png")

def rgb_to_grayscale(red, green, blue):
    return red * 2 + green * 3 + blue

def main():
    (inputFile, outputFile, tileSize, tileOrder) = parse_arguments()

    try:
        with open(inputFile, "rb") as handle:
            uniqueTiles = get_unique_tiles(handle, tileSize)
    except OSError:
        sys.exit("Error reading input file.")

    print("Unique colors:", len(set(chain.from_iterable(uniqueTiles))))
    print("Unique tiles:", len(uniqueTiles))
    print("Min. unique colors/tile:", min(len(set(t)) for t in uniqueTiles))
    print("Max. unique colors/tile:", max(len(set(t)) for t in uniqueTiles))

    if tileOrder == "O":
        pass
    elif tileOrder == "P":
        uniqueTiles.sort(key=lambda t: tuple(rgb_to_grayscale(*p) for p in t))
    elif tileOrder == "A":
        uniqueTiles.sort(key=lambda t: sum(rgb_to_grayscale(*p) for p in t))
    elif tileOrder == "C":
        uniqueTiles.sort(key=lambda t: len(set(t)))
    elif tileOrder == "CP":
        uniqueTiles.sort(key=lambda t: tuple(rgb_to_grayscale(*p) for p in t))
        uniqueTiles.sort(key=lambda t: len(set(t)))
    elif tileOrder == "CA":
        uniqueTiles.sort(key=lambda t: sum(rgb_to_grayscale(*p) for p in t))
        uniqueTiles.sort(key=lambda t: len(set(t)))
    else:
        sys.exit("Something went wrong.")

    try:
        with open(outputFile, "wb") as handle:
            write_image(handle, uniqueTiles, tileSize)
    except OSError:
        sys.exit("Error writing output file.")

main()
