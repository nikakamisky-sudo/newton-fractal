# Monte Carlo: Two Consecutive Ascents

This project estimates the probability that a uniformly random permutation
starts with two consecutive ascents:

```text
pi[0] < pi[1] < pi[2]
```

For every `n >= 3`, the exact probability is `1/6`: the first three values can
appear in any of their six relative orders, and exactly one order is increasing.
The simulation provides a numerical check of that result.

## Setup

Requires Python 3.9 or newer.

```bash
python -m pip install -r requirements.txt
```

## Run

Run the default simulation (one million samples):

```bash
python monte_carlo.py
```

Choose a large permutation size and a reproducible random seed:

```bash
python monte_carlo.py --n 1000000 --samples 2000000 --seed 42
```

The program prints the estimate, its difference from `1/6`, the expected
standard error, and whether the estimate falls within two standard errors of
the exact answer. `--batch-size` controls memory use for large simulations.

The implementation samples only the first three distinct values of each
permutation. This is equivalent to generating a full random permutation for
this event, while avoiding work proportional to `n` for every sample.
