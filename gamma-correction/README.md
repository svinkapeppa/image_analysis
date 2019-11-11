# Gamma correction

Script, that performs [gamma correction algorithm](https://en.wikipedia.org/wiki/Gamma_correction) on given image.

## Notes

- Input image can be colored or grayscale. You should specify the type explicitly,
  otherwise image will be considered colored
- Everything is vectorized

## Pipeline

- Load image
- Translate image values from range [0, 255] to [0, 1]
- Apply formula
- Crop image values so they fit in range [0, 1]
- Scale image values back to [0, 255]
- Round float values correctly
- Save image
  
## Usage

For **colored** images you can use either:

```
python gamma_correction.py data/image.png data/processed.png 1.4 1.4
```

or

```
python gamma_correction.py data/image.png data/processed.png 1.4 1.4 --version colored
```

For **grayscale** images you can use:

```
python gamma_correction.py data/image.png data/processed.png 1.4 1.4 --version grayscale
```

## Examples

Examples can be found in [data](data) directory.
