from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

N = 401  # Grid size
L = 2  # Plotting region: [-2, 2] x [-2, 2]
iters = 50  # Number of Newton iterations

# 1. Create a grid of complex numbers, z = x + iy.
x = np.linspace(-L, L, N)
X, Y = np.meshgrid(x, x)
Z = X + 1j * Y

# 2. Apply Newton's method: z <- z - f(z) / f'(z), for f(z) = z^3 - 1.
# Suppress warnings caused by division by zero and other undefined values.
with np.errstate(all="ignore"):
    for _ in range(iters):
        Z = Z - (Z**3 - 1) / (3 * Z**2)

# 3. Record the angle of the root each point approaches.
# Values at points that do not converge (including z = 0) may be NaN.
result = np.angle(Z)

# 4. Optionally compare the result with a reference file named fractal.npy.
reference_file = Path(__file__).with_name("fractal.npy")
if reference_file.exists():
    reference = np.load(reference_file)
    if reference.shape != result.shape:
        print(
            f"Reference shape {reference.shape} does not match "
            f"the computed result shape {result.shape}; skipping comparison."
        )
    else:
        mask = ~np.isnan(reference) & ~np.isnan(result)
        if mask.any():
            print(np.allclose(reference[mask], result[mask], atol=1e-3))
        else:
            print("No valid values to compare with fractal.npy.")
else:
    print("Reference file fractal.npy not found; skipping comparison.")

# 5. Display the Newton fractal.
plt.imshow(result, origin="lower", extent=[-L, L, -L, L])
plt.title("Newton Fractal: z³ − 1")
plt.xlabel("Re(z)")
plt.ylabel("Im(z)")
plt.show()
