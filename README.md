# unique-tiles
A command-line tool that reads an image and writes another image with distinct tiles (squares of specified size) only.

Some of the sample images are from *Commander Keen: Secret of the Oracle* and *Wolfenstein 3D* by id Software.

## Command-line arguments
*inputFile* *outputFile* *tileSize* *tileOrder*

You may omit the fourth or both the third and the fourth argument.

* *inputFile*: Image file to read (e.g. PNG). The width and height must be multiples of *tileSize*. No alpha channel.
* *outputFile*: PNG file to write. Will contain every distinct tile in *inputFile* once. The width will be 16&times;*tileSize* pixels. The height will be a multiple of *tileSize* pixels.
* *tileSize*: The width and height of each tile, in pixels. 4 to 64. The default is 8.
* *tileOrder*: Order of tiles in the output image. One of these:
  * `O`: original (the first tile to occur in *inputFile* will occur first in *outputFile*; this is the default)
  * `P`: first by brightness of pixels, top left pixel first, then by original order
  * `A`: first by average brightness of each tile, then by original order
  * `C`: first by number of unique colors, then by original order
  * `CP`: first by number of unique colors, then by brightness of pixels, then by original order
  * `CA`: first by number of unique colors, then by average brightness of each tile, then by original order
