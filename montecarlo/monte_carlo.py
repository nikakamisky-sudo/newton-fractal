"""Estimate the probability of two consecutive ascents by Monte Carlo."""

from __future__ import annotations

import argparse
import math
from typing import Optional, Sequence

import numpy as np


THEORETICAL_PROBABILITY = 1 / 6


def starts_with_two_ascents(pi: Sequence[int]) -> bool:
    """Return whether the first three entries are strictly increasing."""
    return len(pi) >= 3 and bool(pi[0] < pi[1] < pi[2])


def monte_carlo_permutations(
    n: int,
    sample_size: int,
    seed: Optional[int] = None,
    batch_size: int = 250_000,
) -> float:
    """Estimate P(pi[0] < pi[1] < pi[2]) for a uniform permutation of 1..n.

    Only the first three values are generated. They are sampled uniformly
    without replacement, which gives exactly the same distribution as the
    first three entries of a full random permutation. Work is batched so large
    simulations use bounded memory.
    """
    if n < 3:
        raise ValueError("n must be at least 3")
    if sample_size <= 0:
        raise ValueError("sample_size must be positive")
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    rng = np.random.default_rng(seed)
    successes = 0

    for start in range(0, sample_size, batch_size):
        current_size = min(batch_size, sample_size - start)

        first = rng.integers(0, n, size=current_size)

        # Map a draw from 0..n-2 around the first value to get a distinct one.
        second_raw = rng.integers(0, n - 1, size=current_size)
        second = second_raw + (second_raw >= first)

        # Map a draw from 0..n-3 around both already selected values.
        lower = np.minimum(first, second)
        upper = np.maximum(first, second)
        third_raw = rng.integers(0, n - 2, size=current_size)
        third = (
            third_raw
            + (third_raw >= lower)
            + (third_raw >= upper - 1)
        )

        successes += int(np.count_nonzero((first < second) & (second < third)))

    return successes / sample_size


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate the chance that a random permutation starts with two ascents."
    )
    parser.add_argument("--n", type=int, default=1_000)
    parser.add_argument("--samples", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=250_000)
    args = parser.parse_args()

    estimate = monte_carlo_permutations(
        n=args.n,
        sample_size=args.samples,
        seed=args.seed,
        batch_size=args.batch_size,
    )
    standard_error = math.sqrt(
        THEORETICAL_PROBABILITY
        * (1 - THEORETICAL_PROBABILITY)
        / args.samples
    )
    difference = estimate - THEORETICAL_PROBABILITY

    print(f"Permutation size n:       {args.n:,}")
    print(f"Monte Carlo samples:      {args.samples:,}")
    print(f"Estimated probability:    {estimate:.8f}")
    print(f"Exact probability:        {THEORETICAL_PROBABILITY:.8f} (1/6)")
    print(f"Absolute error:           {abs(difference):.8f}")
    print(f"Expected standard error:  {standard_error:.8f}")
    print(
        "Estimate within 95% band: "
        f"{abs(difference) <= 1.96 * standard_error}"
    )


if __name__ == "__main__":
    main()
