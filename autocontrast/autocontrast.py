import argparse
import os

import cv2
import numpy as np


def autocontrast(source_path, destination_path, white_percentage, black_percentage, version):
    # Load image into memory
    # Algorithm can work correctly with colored and grayscale images
    if version == 'colored':
        original_image = cv2.imread(source_path)
    elif version == 'grayscale':
        original_image = cv2.imread(source_path, cv2.IMREAD_GRAYSCALE)
    else:
        # Other types are not supported
        raise RuntimeError('Wrong type of image')

    # Histogram will help to find the brightest and the darkest pixels
    hist, _ = np.histogram(original_image.flatten(), 256, [0, 256])

    # `cdf[i]` equals to a number of pixels, which brightness is equal or lower than `i`
    cdf = np.cumsum(hist)

    # Mask pixels, that are too bright / dark
    masked = np.ma.masked_less_equal(cdf, black_percentage * cdf.max())
    masked = np.ma.masked_greater_equal(masked, (1.0 - white_percentage) * cdf.max())

    # `[left, right]` is a range of pixels, that needs to be translated to range [0, 255]
    left = masked.argmin()
    right = masked.argmax()

    mapping = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        if i < left:
            mapping[i] = 0
        elif i > right:
            mapping[i] = 255
        else:
            # Linear translation
            mapping[i] = round((i - left) * 255 / (right - left))

    processed_image = mapping[original_image]

    cv2.imwrite(destination_path, processed_image.astype(np.uint8))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform gamma correction.')
    parser.add_argument('source_path', metavar='source_path', type=str,
                        help='Path to the original image.')
    parser.add_argument('destination_path', metavar='destination_path', type=str,
                        help='Path to the processed image.')
    parser.add_argument('white_percentage', metavar='white_percentage', type=float,
                        help='First parameter of gamma correction algorithm.')
    parser.add_argument('black_percentage', metavar='black_percentage', type=float,
                        help='Second parameter of gamma correction algorithm.')
    parser.add_argument('--version', type=str, default='colored',
                        help='Shows type of image. Variants: colored / grayscale.')

    args = parser.parse_args()

    if not os.path.exists(args.source_path):
        raise FileNotFoundError

    if not 0 <= args.white_percentage < 1:
        raise ValueError

    if not 0 <= args.black_percentage < 1:
        raise ValueError

    autocontrast(args.source_path, args.destination_path, args.white_percentage, args.black_percentage, args.version)
