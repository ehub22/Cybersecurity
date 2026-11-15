"""Tests for the educational MD5 hash cracker."""

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "Git Repository"
sys.path.insert(0, str(SCRIPT_DIR))

from Cracker import DEFAULT_ALPHABET, crack_hash, cracker, md5_hexdigest  # noqa: E402


class HashCrackerTests(unittest.TestCase):
    def test_md5_helper_returns_known_digest(self):
        self.assertEqual(md5_hexdigest("abc"), "900150983cd24fb0d6963f7d28e17f72")

    def test_cracks_hashes_of_various_lengths(self):
        self.assertEqual(crack_hash(md5_hexdigest("a"), 1, 1), "a")
        self.assertEqual(crack_hash(md5_hexdigest("abc"), 1, 3), "abc")
        # This character was missing from the original default alphabet.
        self.assertIn("q", DEFAULT_ALPHABET)
        self.assertEqual(crack_hash(md5_hexdigest("q"), 1, 1), "q")

    def test_returns_none_for_a_miss(self):
        self.assertIsNone(crack_hash(md5_hexdigest("c"), 1, 1, alphabet="ab"))

    def test_legacy_function_name_uses_explicit_arguments(self):
        self.assertEqual(cracker(md5_hexdigest("ab"), 1, 2, alphabet="ab"), "ab")

    def test_rejects_bad_hashes_lengths_and_alphabets(self):
        for target in ("", "not an md5 hash", "0" * 31):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    crack_hash(target, 1, 2)
        with self.assertRaises(ValueError):
            crack_hash("0" * 32, 2, 1)
        with self.assertRaises(ValueError):
            crack_hash("0" * 32, 1, 2, alphabet="")
        with self.assertRaises(TypeError):
            crack_hash("0" * 32, "1", 2)


if __name__ == "__main__":
    unittest.main()
