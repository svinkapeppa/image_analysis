# Otsu binarization

Script, that binarize given image with [Otsu algorithm](https://en.wikipedia.org/wiki/Otsu%27s_method).

## Pipeline

- Load image
- Make it to grayscale
- Calculate histogram
- Iterate through every threshold and choose the best using the following criteria:
  based on the given threshold intercalss variance is the greatest
- Binarize image using the best threshold
- Save image

## Usage

```
python otsu.py data/image.png data/processed.png
```

## Examples

Examples can be found in [data](data) directory.
