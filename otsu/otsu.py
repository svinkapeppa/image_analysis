import argparse
import os

import cv2
import numpy as np


def otsu(source_path, destination_path):
    # Load image into memory. Convert it to grayscale
    image = cv2.imread(source_path, cv2.IMREAD_GRAYSCALE)

    # Calculate histogram and center of the bins
    hist, edges = np.histogram(image.flatten(), 256, [0, 256])

    # Last edge is redundant
    edges = edges[:-1]

    # Precalculate everything in a vectorized style
    cdf = np.cumsum(hist)
    area = np.cumsum(hist * edges)

    # Placeholders for best split
    max_sigma = None
    threshold = None

    # Last threshold value is ommited
    for t in range(len(edges) - 1):
        # Parameters of current threshold
        alpha = area[t]
        beta = cdf[t]

        # Probability of the first class
        p = beta / cdf[-1]

        # Calculate interclass variance
        a = alpha / beta - (area[-1] - alpha) / (cdf[-1] - beta)
        sigma = p * (1 - p) * a * a

        # Choose threshold with biggest variance
        if not max_sigma or sigma > max_sigma:
            max_sigma = sigma
            threshold = t

    # Binarize image
    image[image <= threshold] = 0
    image[image > threshold] = 255

    cv2.imwrite(destination_path, image.astype(np.uint8))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform otsu binarization.')
    parser.add_argument('source_path', metavar='source_path', type=str,
                        help='Path to the original image.')
    parser.add_argument('destination_path', metavar='destination_path', type=str,
                        help='Path to the processed image.')

    args = parser.parse_args()

    if not os.path.exists(args.source_path):
        raise FileNotFoundError

    otsu(args.source_path, args.destination_path)
