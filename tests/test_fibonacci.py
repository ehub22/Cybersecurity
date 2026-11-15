"""Tests for Fibonacci sequence generation."""

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "Git Repository"
sys.path.insert(0, str(SCRIPT_DIR))

from Fibonacci import calc_fib, fibonacci  # noqa: E402


class FibonacciTests(unittest.TestCase):
    def test_returns_first_n_values(self):
        self.assertEqual(calc_fib(7), [0, 1, 1, 2, 3, 5, 8])
        self.assertEqual(fibonacci(5), [0, 1, 1, 2, 3])

    def test_zero_and_one(self):
        self.assertEqual(calc_fib(0), [])
        self.assertEqual(calc_fib(1), [0])

    def test_repeated_calls_are_independent(self):
        self.assertEqual(calc_fib(5), [0, 1, 1, 2, 3])
        self.assertEqual(calc_fib(2), [0, 1])
        self.assertEqual(calc_fib(5), [0, 1, 1, 2, 3])

    def test_rejects_invalid_sizes(self):
        for size in (-1, -10):
            with self.subTest(size=size):
                with self.assertRaises(ValueError):
                    calc_fib(size)
        for size in (1.5, "3", True):
            with self.subTest(size=size):
                with self.assertRaises(TypeError):
                    calc_fib(size)


if __name__ == "__main__":
    unittest.main()
