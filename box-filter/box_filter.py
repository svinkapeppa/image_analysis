import argparse
import os

import cv2
import numpy as np


def box_filter(source_path, destination_path, width, height, version):
    # Load image into memory
    # Algorithm can work correctly with colored and grayscale images
    if version == 'colored':
        image = cv2.imread(source_path)
    elif version == 'grayscale':
        image = cv2.imread(source_path, cv2.IMREAD_GRAYSCALE)
    else:
        # Other types are not supported
        raise RuntimeError('Wrong type of image')

    processed = np.zeros(image.shape, dtype=np.uint8)

    # Complexity: O(N), N - number of pixels
    integral = np.cumsum(np.cumsum(image, axis=1), axis=0)

    # Complexity: O(N), N - number of pixels
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            # Pixel lies in the center of the filter, so we need to
            # go half time to the left / right / up / down
            w = width // 2
            h = height // 2

            left = max(col - w, 0)
            right = min(col + w, image.shape[1] - 1)
            top = max(row - h, 0)
            bot = min(row + h, image.shape[0] - 1)

            area = (bot - top) * (right - left)
            value = integral[bot][right] - integral[top][right] - integral[bot][left] + integral[top][left]
            value = np.rint(value / area)

            processed[row, col] = value

    # Crop values, that are too high
    processed[processed >= 255] = 255

    cv2.imwrite(destination_path, processed.astype(np.uint8))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply box-filter.')
    parser.add_argument('source_path', metavar='source_path', type=str,
                        help='Path to the original image.')
    parser.add_argument('destination_path', metavar='destination_path', type=str,
                        help='Path to the processed image.')
    parser.add_argument('width', metavar='width', type=int,
                        help='Width of the box-filter.')
    parser.add_argument('height', metavar='height', type=int,
                        help='Height of the box-filter.')
    parser.add_argument('--version', type=str, default='colored',
                        help='Shows type of image. Variants: colored / grayscale.')

    args = parser.parse_args()

    if not os.path.exists(args.source_path):
        raise FileNotFoundError

    if args.width <= 0:
        raise ValueError

    if args.height <= 0:
        raise ValueError

    box_filter(args.source_path, args.destination_path, args.width, args.height, args.version)
