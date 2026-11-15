"""Tests for the Vigenere cipher module."""

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "Git Repository"
sys.path.insert(0, str(SCRIPT_DIR))

from vcipher import decrypt, encrypt, generate_key  # noqa: E402


class VigenereCipherTests(unittest.TestCase):
    def test_generate_key_repeats_and_preserves_case(self):
        self.assertEqual(generate_key("Hello", "Hi"), "HiHiH")
        self.assertEqual(generate_key("", "Hi"), "")

    def test_encrypt_and_decrypt(self):
        self.assertEqual(encrypt("Hello", "Hi"), "Omstv")
        self.assertEqual(decrypt("Omstv", "Hi"), "Hello")

    def test_case_and_punctuation_are_preserved(self):
        text = "Hello, World!"
        self.assertEqual(decrypt(encrypt(text, "Key"), "Key"), text)
        self.assertEqual(encrypt("A a!", "B"), "B b!")

    def test_non_ascii_characters_are_not_shifted(self):
        self.assertEqual(encrypt("Café!", "abc"), "Cbhé!")

    def test_invalid_keys_are_rejected(self):
        for key in ("", "123!", "é"):
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    encrypt("text", key)
        with self.assertRaises(TypeError):
            encrypt("text", None)


if __name__ == "__main__":
    unittest.main()
