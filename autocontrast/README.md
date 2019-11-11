# Autocontrast

Script, that performs automatic brightness correction on given image.

## Notes

- Input image can be colored or grayscale. You should specify the type explicitly,
  otherwise image will be considered colored
- Everything is vectorized (except linear mapping)

## Pipeline

- Load image
- Calculate histogram
- Calculate number of pixels that are greater than a threshold for every threshold
- Calculate cutoff pixels
- Linearly scale pixels
- Save image

## Usage

For **colored** images you can use either:

```
python autocontrast.py data/image.png data/processed.png 0.1 0.01
```

or

```
python autocontrast.py data/image.png data/processed.png 0.1 0.01 --version colored
```

For **grayscale** images you can use:

```
python autocontrast.py data/image.png data/processed.png 0.1 0.01 --version grayscale
```

## Examples

Examples can be found in [data](data) directory.
