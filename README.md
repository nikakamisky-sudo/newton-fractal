# Function Visualisation

A small Python project that visualizes the Newton fractal for the function
`f(z) = z³ − 1` over the complex plane.

The script applies Newton's method to every point on a two-dimensional grid.
It colors each point according to the angle of the root it approaches. The
three roots are `1` and `−1/2 ± (√3/2)i`.

## Requirements

- Python 3.9 or newer
- NumPy
- Matplotlib

Install the Python packages with:

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python newton_fractal.py
```

The script opens a Matplotlib window with the fractal. Its default settings use
a `401 × 401` grid, cover `[-2, 2] × [-2, 2]`, and perform 50 Newton iterations.

## Optional reference comparison

To compare the computed angles with a saved result, place a compatible NumPy
array named `fractal.npy` next to `newton_fractal.py`. The array must have the
same shape as the generated grid. If the file is absent, the comparison is
skipped and the fractal is still displayed.
