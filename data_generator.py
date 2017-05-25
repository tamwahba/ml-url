import json
import os
import random
from random import randint
import string

import numpy
from PIL import Image, ImageDraw, ImageFont

from random_urls import random_chars

CHARACTERS = string.ascii_letters + string.digits + string.punctuation
FONTS = ['arial.ttf', 'segoeui.ttf', 'tahoma.ttf']


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append(
            [p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append(
            [0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def generate_letters(directory, count=1000):
    os.makedirs(directory, exist_ok=True)
    os.makedirs('./letters/test/', exist_ok=True)
    mapping = {}
    counter = 0

    # generate baseline images
    for c in CHARACTERS:
        for f in FONTS:
            font_name = f.split('.')[0]
            mapping[counter] = {'font': font_name, 'character': c}
            with open('{0}/{1}.jpeg'.format(directory, counter), 'w') as file:
                im = Image.new('RGB', (50, 50), (255, 255, 255))
                draw = ImageDraw.Draw(im)
                font = ImageFont.truetype(f, 40)

                s = draw.textsize(c, fill=(0, 0, 0), font=font)
                x = (50 - s[0]) / 2
                y = (50 - s[1]) / 2

                draw.text((x, y), c,
                          fill=(0, 0, 0), font=font)

                im.save(file, 'jpeg')
                counter += 1

    # generate warped images
    for c in random_chars(count, CHARACTERS):
        f = random.choice(FONTS)
        font_name = f.split('.')[0]
        mapping[counter] = {'font': font_name, 'character': c}

        with open('{0}/{1}.jpeg'.format(directory, counter), 'w') as file:
            im = Image.new('RGB', (50, 50), (255, 255, 255))
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype(f, randint(25, 35))

            s = draw.textsize(c, fill=(0, 0, 0), font=font)
            x = (50 - s[0]) / 2
            y = (50 - s[1]) / 2

            draw.text((x, y), c,
                      fill=(0, 0, 0), font=font)

            coeffs = find_coeffs(
                [(0, 0), (50, 0), (50, 50), (0, 50)],
                [(randint(0, 10), randint(0, 10)),
                 (randint(50 - 10, 50), randint(0, 10)),
                 (randint(50 - 10, 50), randint(50 - 10, 50)),
                 (randint(0, 10), randint(50 - 10, 50))])
            im.transform(
                im.size, Image.PERSPECTIVE, coeffs).save(file, 'jpeg')

            counter += 1

    with open('{0}/mapping.json'.format(directory), 'w') as file:
        file.write(json.dumps(mapping))


if __name__ == '__main__':
    random.seed(0)  # determistic data generation
    generate_letters('./letters/train/', 5000)
    generate_letters('./letters/test/', 20000)
