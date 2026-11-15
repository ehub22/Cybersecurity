"""Fibonacci sequence generator.

Examples::

    >>> calc_fib(7)
    [0, 1, 1, 2, 3, 5, 8]
    >>> fibonacci(5)
    [0, 1, 1, 2, 3]

Command line::

    python Fibonacci.py 10
    python Fibonacci.py --count 10

Importing this module has no side effects: no numbers are printed
until you call a function or run the script.
"""

from __future__ import annotations

import argparse
import sys
import time


def calc_fib(size: int) -> list[int]:
    """Return the first *size* Fibonacci numbers starting with 0, 1.

    Args:
        size: How many numbers to generate. Must be >= 0.

    Returns:
        A list of length *size*, e.g. ``calc_fib(5) == [0, 1, 1, 2, 3]``.
        ``calc_fib(0)`` returns ``[]`` and ``calc_fib(1)`` returns ``[0]``.

    Raises:
        TypeError: If *size* is not an integer.
        ValueError: If *size* is negative.
    """
    if isinstance(size, bool) or not isinstance(size, int):
        raise TypeError("size must be an integer")
    if size < 0:
        raise ValueError("size must be non-negative")

    numbers: list[int] = []
    a, b = 0, 1
    for _ in range(size):
        numbers.append(a)
        a, b = b, a + b
    return numbers


def fibonacci(n: int) -> list[int]:
    """Alias for :func:`calc_fib` with a more descriptive name."""
    return calc_fib(n)


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Print the first N Fibonacci numbers."
    )
    parser.add_argument(
        "count",
        nargs="?",
        type=int,
        help="How many numbers to print (default: 10).",
    )
    parser.add_argument(
        "-n",
        "--count",
        dest="option_count",
        type=int,
        help="How many numbers to print (alternative to the positional count).",
    )
    args = parser.parse_args(argv)
    if args.count is not None and args.option_count is not None:
        parser.error("provide the count either positionally or with --count, not both")
    count = args.option_count
    if count is None:
        count = args.count if args.count is not None else 10

    start = time.perf_counter()
    try:
        numbers = calc_fib(count)
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))
    elapsed = time.perf_counter() - start

    for value in numbers:
        print(value)
    print(f"Elapsed time: {elapsed:.6f}s", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
