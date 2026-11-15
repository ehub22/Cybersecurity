"""Vigenere cipher encryption and decryption.

The Vigenere cipher shifts each letter by an amount determined by a
repeating keyword. Letter case is preserved and non-alphabetic
characters are left unchanged (and do not advance the keyword).

Examples::

    >>> generate_key("Hello", "Hi")
    'HiHiH'
    >>> encrypt("Hello", "Hi")
    'Omstv'
    >>> decrypt("Omstv", "Hi")
    'Hello'

Command line::

    python vcipher.py encrypt "Hello" --key Hi
    python vcipher.py decrypt "Opnvs" --key Hi

Importing this module has no side effects: nothing is printed and no
input is requested until you call a function or run the script.
"""

from __future__ import annotations

import argparse
import sys


def _key_letters(key: str) -> str:
    """Return the ASCII letters in *key*, preserving case."""
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    letters = "".join(
        char for char in key
        if "a" <= char <= "z" or "A" <= char <= "Z"
    )
    if not letters:
        raise ValueError("key must contain at least one ASCII letter")
    return letters


def _validate_key(key: str) -> str:
    """Return the upper-cased ASCII key or raise a useful error."""
    return _key_letters(key).upper()


def generate_key(string: str, key: str) -> str:
    """Repeat *key* to match the length of *string*.

    Args:
        string: The text whose length determines the output length.
        key: The keyword to repeat. Must contain at least one letter.

    Returns:
        A string of length ``len(string)`` made by repeating the
        alphabetic characters of *key*, e.g.
        ``generate_key("Hello", "Hi") == "HiHiH"``.

    Raises:
        TypeError: If either argument is not a string.
        ValueError: If *key* contains no ASCII letters.
    """
    if not isinstance(string, str):
        raise TypeError("string must be a string")
    clean_key = _key_letters(key)
    if not string:
        return ""
    key_len = len(clean_key)
    return "".join(clean_key[i % key_len] for i in range(len(string)))


def _crypt(text: str, key: str, direction: int) -> str:
    """Shared encrypt/decrypt logic; *direction* is +1 or -1."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    clean_key = _validate_key(key)
    key_len = len(clean_key)
    result: list[str] = []
    key_index = 0
    for char in text:
        if "a" <= char <= "z":
            base = ord("a")
            shift = ord(clean_key[key_index % key_len]) - ord("A")
            result.append(
                chr((ord(char) - base + direction * shift) % 26 + base)
            )
            key_index += 1
        elif "A" <= char <= "Z":
            base = ord("A")
            shift = ord(clean_key[key_index % key_len]) - ord("A")
            result.append(
                chr((ord(char) - base + direction * shift) % 26 + base)
            )
            key_index += 1
        else:
            result.append(char)
    return "".join(result)


def encrypt(text: str, key: str) -> str:
    """Encrypt *text* with the Vigenere cipher using *key*."""
    return _crypt(text, key, +1)


def decrypt(text: str, key: str) -> str:
    """Decrypt *text* previously encrypted with :func:`encrypt`."""
    return _crypt(text, key, -1)


# Descriptive aliases.
vigenere_encrypt = encrypt
vigenere_decrypt = decrypt
cipher_text = encrypt


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt text with a Vigenere cipher."
    )
    parser.add_argument(
        "mode",
        choices=["encrypt", "decrypt"],
        help="Whether to encrypt or decrypt.",
    )
    parser.add_argument("text", help="Text to process.")
    parser.add_argument(
        "--key",
        required=True,
        help="Keyword, e.g. --key Hi (must contain at least one letter).",
    )
    args = parser.parse_args(argv)

    try:
        if args.mode == "encrypt":
            print(encrypt(args.text, args.key))
        else:
            print(decrypt(args.text, args.key))
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
