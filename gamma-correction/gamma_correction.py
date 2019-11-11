import argparse
import os

import cv2
import numpy as np


def gamma_correction(source_path, destination_path, a, b, version):
    # Load image into memory
    # Algorithm can work correctly with colored and grayscale images
    if version == 'colored':
        original_image = cv2.imread(source_path)
    elif version == 'grayscale':
        original_image = cv2.imread(source_path, cv2.IMREAD_GRAYSCALE)
    else:
        # Other types are not supported
        raise RuntimeError('Wrong type of image')

    # Apply formula to rescaled image
    processed_image = a * ((original_image / 255) ** b)
    # Crop values, that are too high
    processed_image[processed_image >= 1] = 1
    # Scale image back to [0 - 255]
    processed_image = processed_image * 255
    # Correctly convert float values to integers
    processed_image = np.rint(processed_image)

    # Convert to `np.uint8`, so `imwrite` will save image correctly
    cv2.imwrite(destination_path, processed_image.astype(np.uint8))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform gamma correction.')
    parser.add_argument('source_path', metavar='source_path', type=str,
                        help='Path to the original image.')
    parser.add_argument('destination_path', metavar='destination_path', type=str,
                        help='Path to the processed image.')
    parser.add_argument('a', metavar='a', type=float,
                        help='First parameter of gamma correction algorithm.')
    parser.add_argument('b', metavar='b', type=float,
                        help='Second parameter of gamma correction algorithm.')
    parser.add_argument('--version', type=str, default='colored',
                        help='Shows type of image. Variants: colored / grayscale.')

    args = parser.parse_args()

    if not os.path.exists(args.source_path):
        raise FileNotFoundError

    gamma_correction(args.source_path, args.destination_path, args.a, args.b, args.version)
