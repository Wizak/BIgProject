from PIL import Image

import os


def resize_photo(dir):
    for filename in os.listdir(dir):
        filename = f'{dir}/{filename}'
        image = Image.open(filename)
        image = image.resize((150, 150))
        image.save(filename)


if __name__ == '__main__':
    dirs = ['mobs/train/images', 'mobs/validation/images']
    [resize_photo(dir) for dir in dirs]