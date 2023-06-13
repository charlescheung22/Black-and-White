import os
from random import choice
from PIL import Image, ImageOps

# Constants
BORDER_SIZE = 72  # Border surrounding final picture
SPACING = 8  # Spacing in between every tile
IMAGE_SIZE = 128  # Side length on one image tile
WIDTH = 4  # Number of tiles length-wise
HEIGHT = 8  # Number of tiles height-wise

# Image packs to be used:

class ImagePack:
    def __init__(self, number: int, use: bool, invert: bool, rotate: bool, source: str) -> None:
        # TODO: image weighting
        self.number = number  # Specify which image pack
        self.use = use  # use this image pack
        self.invert = invert  # randomly invert colors
        self.rotate = rotate  # randomly rotate images
        self.source = source  # Directory location
        self.collection = dict()

        # Process images
        with os.scandir(self.source) as directory_ls:
            for subdirectory in directory_ls:
                if subdirectory.name != "info" and subdirectory.is_dir():
                    with os.scandir(self.source + "\\" + subdirectory.name) as subdirectory_ls:
                        self.collection[subdirectory.name] = []
                        for file in subdirectory_ls:
                            if os.path.isfile(file):
                                self.collection.get(subdirectory.name).append(Image.open(self.source + "\\" + subdirectory.name + "\\" + file.name))

    def choice_unweighted(self) -> Image:
        return choice(self.collection.get(choice(list(self.collection.keys()))))





if __name__ == "__main__":

    # Setup
    ImagePackOne = ImagePack(1, True, True, True, "image pack 1")
    ImagePacks = [ImagePackOne]

    # Create a Pillow Image
    im = Image.new(mode="L", size=(2*BORDER_SIZE + (WIDTH + 1)*SPACING + WIDTH*IMAGE_SIZE, 2*BORDER_SIZE + (HEIGHT+1)*SPACING + HEIGHT*IMAGE_SIZE), color=(255,))

    # Choose and insert image tiles from selections  # IN ORDER
    for i in range(WIDTH):
        for j in range(HEIGHT):
            pixel_position = ((BORDER_SIZE + (i+1)*SPACING + i*IMAGE_SIZE) + 1, (BORDER_SIZE + (j+1)*SPACING + j*IMAGE_SIZE) + 1)  # Since pixels start at (1, 1)

            pack = choice(ImagePacks)
            tile = pack.choice_unweighted()
            tile = tile.convert("L")  # Conversion to Luminance mode to save memory: stores grayscale
            tile = tile.resize(size=(IMAGE_SIZE, IMAGE_SIZE))
            if pack.invert and choice([False, True]):  # half and half chance
                ImageOps.invert(tile)
            if pack.rotate:
                angle = choice([False, 90, 180, 270])
                if angle:  # angle must be an integer degrees
                    tile = tile.rotate(angle)


            im.paste(tile, box=pixel_position)


    # # Choose RANDOMLY and insert image tiles from selections  # TODO Can put in larger tiles of images later
    # tile_tracker = [[False for j in range(HEIGHT)] for i in range(WIDTH)]  # represents a grid of which spaces where there are tiles iff True



    # Finally, either save the image or show it.
    im.show()







