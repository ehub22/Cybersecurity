"""Caesar cipher encryption and decryption.

A Caesar cipher shifts ASCII letters by a fixed amount, wrapping around
the alphabet (``a`` -> ``d`` with a shift of 3, ``z`` -> ``c``).
Letter case is preserved and non-ASCII characters or punctuation are
left unchanged.

Examples::

    >>> encrypt("Hello", 3)
    'Khoor'
    >>> decrypt("Khoor", 3)
    'Hello'

Command line::

    python Cesar_Encrypter.py encrypt "Hello" --shift 3
    python Cesar_Encrypter.py decrypt "Khoor" --shift 3
    python Cesar_Encrypter.py encrypt --shift 3   # prompts for input

Importing this module has no side effects: nothing is printed and no
input is requested until you call a function or run the script.
"""

from __future__ import annotations

import argparse
import sys

DEFAULT_SHIFT = 3


def _shift_text(text: str, shift: int) -> str:
    """Shift each ASCII letter in *text* by *shift* places."""
    shift %= 26
    if shift == 0:
        return text
    result: list[str] = []
    for char in text:
        if "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= char <= "Z":
            result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        else:
            result.append(char)
    return "".join(result)


def encrypt(text: str | None = None, shift: int = DEFAULT_SHIFT) -> str:
    """Encrypt *text* with a Caesar shift.

    Args:
        text: The plaintext to encrypt. If ``None`` (the legacy
            interactive behaviour), the user is prompted with
            ``input("Enter password: ")``.
        shift: Number of positions to shift by. Any integer is
            accepted; it is reduced modulo 26.

    Returns:
        The encrypted text.
    """
    if text is None:
        text = input("Enter password: ")
    return _shift_text(text, shift)


def decrypt(text: str | None = None, shift: int = DEFAULT_SHIFT) -> str:
    """Decrypt *text* previously encrypted with :func:`encrypt`.

    Args:
        text: The ciphertext to decrypt. If ``None``, the user is
            prompted with ``input("Enter password: ")``.
        shift: The same shift used for encryption.

    Returns:
        The decrypted plaintext.
    """
    if text is None:
        text = input("Enter password: ")
    return _shift_text(text, -shift)


# Descriptive aliases.
caesar_encrypt = encrypt
caesar_decrypt = decrypt


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt text with a Caesar cipher."
    )
    parser.add_argument(
        "mode",
        choices=["encrypt", "decrypt"],
        help="Whether to encrypt or decrypt.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to process. If omitted, you will be prompted for it.",
    )
    parser.add_argument(
        "--shift",
        type=int,
        default=DEFAULT_SHIFT,
        help="Shift amount (default: %(default)s).",
    )
    args = parser.parse_args(argv)

    text = args.text
    if text is None:
        text = input("Enter password: ")

    if args.mode == "encrypt":
        print(encrypt(text, args.shift))
    else:
        print(decrypt(text, args.shift))
    return 0


if __name__ == "__main__":
    sys.exit(main())
