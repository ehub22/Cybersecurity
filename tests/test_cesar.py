"""Tests for the Caesar cipher module."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "Git Repository"
sys.path.insert(0, str(SCRIPT_DIR))

from Cesar_Encrypter import decrypt, encrypt  # noqa: E402


class CaesarCipherTests(unittest.TestCase):
    def test_encrypt_and_decrypt(self):
        self.assertEqual(encrypt("Hello", 3), "Khoor")
        self.assertEqual(decrypt("Khoor", 3), "Hello")

    def test_wraps_alphabet_and_preserves_case(self):
        self.assertEqual(encrypt("xyz XYZ", 3), "abc ABC")
        self.assertEqual(decrypt("abc ABC", 3), "xyz XYZ")

    def test_non_letters_are_unchanged(self):
        self.assertEqual(encrypt("Hello, world! 123", 3), "Khoor, zruog! 123")

    def test_large_and_negative_shifts(self):
        self.assertEqual(encrypt("abc", 29), "def")
        self.assertEqual(decrypt("def", 29), "abc")
        self.assertEqual(encrypt("abc", -1), "zab")

    def test_encrypt_prompts_when_text_is_omitted(self):
        with patch("builtins.input", return_value="abc") as prompt:
            self.assertEqual(encrypt(), "def")
        prompt.assert_called_once_with("Enter password: ")


if __name__ == "__main__":
    unittest.main()
