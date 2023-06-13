import os
from random import choice
from PIL import Image, ImageOps


# Constants
BORDER_SIZE = 72    # Border surrounding final picture
SPACING = 8         # Spacing in between every tile
IMAGE_SIZE = 128    # Side length on one image tile
WIDTH = 4           # Number of tiles length-wise
HEIGHT = 8          # Number of tiles height-wise


# Image packs to be used:
class ImagePack:
    """This class contains all the images needed. Instantiate this once to get images."""
    def __init__(self, invert: bool, rotate: bool, sources: list[str]) -> None:
        # TODO: image weighting
        self.invert = invert  # randomly invert colors
        self.rotate = rotate  # randomly rotate images
        self.sources = sources  # Directory location
        self.collection = dict()

        # Process images
        # Assumed path location: ".\ImagePacks\ImagePack1...etc\1x1, info, etc\123.png # TODO get rid of shitty hardcode
        with os.scandir("ImagePacks") as main_imgp:
            for dir_imgp in main_imgp:
                if dir_imgp.is_dir() and dir_imgp.name in self.sources:
                    self.collection[dir_imgp.name] = []
                    with os.scandir(str("ImagePacks" + "\\" + dir_imgp.name)) as sub_dir_imgp:
                        for side_dir_imgp in sub_dir_imgp:
                            if side_dir_imgp.is_dir() and side_dir_imgp.name != "info":
                                with os.scandir(str("ImagePacks" + "\\" + dir_imgp.name + "\\" + side_dir_imgp.name)) as sub_sub_dir_imgp:
                                    for file in sub_sub_dir_imgp:
                                        if file.is_file():
                                            self.collection.get(dir_imgp.name).append(Image.open("ImagePacks" + "\\" + dir_imgp.name + "\\" + side_dir_imgp.name + "\\" + file.name))


    def choice_unweighted(self) -> Image:
        return choice(self.collection.get(choice(list(self.collection.keys()))))



if __name__ == "__main__":

    # Setup
    pack = ImagePack(True, True, ["ImagePack1 - corners", "ImagePack2 - arrows", "ImagePack3 - curves"])

    # Create a Pillow Image
    im = Image.new(mode="L", size=(2*BORDER_SIZE + (WIDTH + 1)*SPACING + WIDTH*IMAGE_SIZE, 2*BORDER_SIZE + (HEIGHT+1)*SPACING + HEIGHT*IMAGE_SIZE), color=(255,))

    # Choose and insert image tiles from selections  # IN ORDER
    for i in range(WIDTH):
        for j in range(HEIGHT):
            pixel_position = ((BORDER_SIZE + (i+1)*SPACING + i*IMAGE_SIZE) + 1, (BORDER_SIZE + (j+1)*SPACING + j*IMAGE_SIZE) + 1)  # Since pixels start at (1, 1)

            tile = pack.choice_unweighted()
            tile = tile.convert("L")  # Conversion to Luminance mode to save memory: stores grayscale
            tile = tile.resize(size=(IMAGE_SIZE, IMAGE_SIZE))
            if pack.invert and choice([False, True]):  # half-and-half chance
                tile = ImageOps.invert(tile)
            if pack.rotate:
                angle = choice([False, 90, 180, 270])
                if angle:  # angle must be an integer degrees
                    tile = tile.rotate(angle)


            im.paste(tile, box=pixel_position)


    # # Choose RANDOMLY and insert image tiles from selections  # TODO Can make it work with putting in larger tiles of images later
    # tile_tracker = [[False for j in range(HEIGHT)] for i in range(WIDTH)]  # represents a grid of which spaces where there are tiles iff True


    # Finally, either save the image or show it.
    im.show()







