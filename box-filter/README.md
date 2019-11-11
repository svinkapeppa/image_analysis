# Box filter

Script, that applies [box-filter](https://en.wikipedia.org/wiki/Box_blur) to given image.

## Notes

- Input image can be colored or grayscale. You should specify the type explicitly,
  otherwise image will be considered colored
- Time complexity is `O(N)`, where `N` is a total number of pixels

## Pipeline

- Load image
- Calculate image integral
- For every pixel of new image calculate values via non-trivial formula
- Save image

## Usage

For **colored** images you can use either:

```
python box_filter.py data/image.png data/processed.png 11 11
```

or

```
python box_filter.py data/image.png data/processed.png 11 11 --version colored
```

For **grayscale** images you can use:

```
python box_filter.py data/image.png data/processed.png 11 11 --version grayscale
```

## Examples

Examples can be found in [data](data) directory.
