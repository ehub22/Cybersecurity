"""Brute-force MD5 password cracker (educational use only).

Given an MD5 hex digest, this module tries every combination of
letters from an alphabet up to a maximum length until it finds a
candidate whose MD5 matches.

.. warning::
    MD5 is cryptographically broken and must never be used to protect
    real passwords. This cracker exists for learning and CTF-style
    exercises only. Do not use it against passwords or hashes you do
    not own or have explicit permission to test.

Examples::

    >>> digest = md5_hexdigest("abc")
    >>> crack_hash(digest, 1, 3)
    'abc'

Command line::

    # Crack a known hash:
    python Cracker.py --hash 900150983cd24fb0d6963f7d28e17f72 --min-length 1 --max-length 4

    # Hash a password and then crack it back (demo):
    python Cracker.py --password abc --min-length 1 --max-length 4

Importing this module has no side effects: nothing is printed and no
input is requested until you call a function or run the script.
"""

from __future__ import annotations

import argparse
import hashlib
import string
import sys
from itertools import product

# Fixed alphabet: the original missed j, q, x and z.
DEFAULT_ALPHABET = string.ascii_lowercase + "!"


def md5_hexdigest(password: str) -> str:
    """Return the MD5 hex digest of *password*.

    Uses ``usedforsecurity=False`` where supported so the demo still
    works on FIPS-enabled systems. MD5 remains insecure regardless.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    data = password.encode()
    try:
        return hashlib.md5(data, usedforsecurity=False).hexdigest()
    except TypeError:  # Python < 3.9
        return hashlib.md5(data).hexdigest()


def _validate_lengths(min_length: int, max_length: int) -> None:
    if isinstance(min_length, bool) or not isinstance(min_length, int):
        raise TypeError("min_length must be an integer")
    if isinstance(max_length, bool) or not isinstance(max_length, int):
        raise TypeError("max_length must be an integer")
    if min_length < 0:
        raise ValueError("min_length must be non-negative")
    if max_length < min_length:
        raise ValueError("max_length must be >= min_length")


def crack_hash(
    target_hash: str,
    min_length: int,
    max_length: int,
    alphabet: str = DEFAULT_ALPHABET,
) -> str | None:
    """Brute-force *target_hash* (an MD5 hex digest).

    Args:
        target_hash: 32-character MD5 hex digest to crack.
        min_length: Shortest candidate length to try (inclusive).
        max_length: Longest candidate length to try (inclusive).
        alphabet: Characters to try, in order.

    Returns:
        The first password found, or ``None`` if no candidate in the
        search space matches.

    Raises:
        TypeError: If lengths are not integers.
        ValueError: If lengths are invalid, the alphabet is empty, or
            the hash is not a 32-character hex string.
    """
    _validate_lengths(min_length, max_length)
    if not isinstance(target_hash, str):
        raise TypeError("target_hash must be a string")
    target = target_hash.strip().lower()
    if len(target) != 32 or any(c not in "0123456789abcdef" for c in target):
        raise ValueError("target_hash must be a 32-character MD5 hex digest")
    if not isinstance(alphabet, str):
        raise TypeError("alphabet must be a string")
    if not alphabet:
        raise ValueError("alphabet must not be empty")

    for length in range(min_length, max_length + 1):
        for possibility in product(alphabet, repeat=length):
            candidate = "".join(possibility)
            if md5_hexdigest(candidate) == target:
                return candidate
    return None


def cracker(
    target_hash: str,
    min_length: int,
    max_length: int,
    alphabet: str = DEFAULT_ALPHABET,
) -> str | None:
    """Legacy-name wrapper around :func:`crack_hash`.

    The original ``cracker()`` took no arguments and read global
    variables set by top-level ``input()`` calls. This wrapper takes
    explicit arguments, matching :func:`crack_hash`.
    """
    return crack_hash(target_hash, min_length, max_length, alphabet)


def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="Brute-force an MD5 hash (educational use only)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--hash",
        help="MD5 hex digest to crack, e.g. 900150983cd24fb0d6963f7d28e17f72.",
    )
    group.add_argument(
        "--password",
        help="Password to hash first, then crack (demo mode).",
    )
    parser.add_argument(
        "--min-length",
        type=int,
        default=1,
        help="Shortest candidate length (default: %(default)s).",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=4,
        help="Longest candidate length (default: %(default)s).",
    )
    parser.add_argument(
        "--alphabet",
        default=DEFAULT_ALPHABET,
        help="Characters to try (default: %(default)s).",
    )
    args = parser.parse_args(argv)

    if args.password is not None:
        target = md5_hexdigest(args.password)
        print(f"MD5({args.password!r}) = {target}")
    else:
        target = args.hash

    try:
        found = crack_hash(
            target, args.min_length, args.max_length, args.alphabet
        )
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))

    if found is None:
        print("Error. No password found.")
        return 1
    print("Password found: " + found)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
