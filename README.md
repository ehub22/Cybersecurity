# Cybersecurity

Small Python learning project covering classic ciphers, a brute-force
MD5 cracker demo, and the Fibonacci sequence. No third-party
dependencies — everything runs on the Python standard library.

## Repository layout

```
Cybersecurity/
├── hello.py                  # Hello World example
├── README.md                 # This file
├── .gitignore
├── Git Repository/           # Learning scripts (original folder name)
│   ├── Cesar_Encrypter.py    # Caesar cipher (encrypt / decrypt)
│   ├── Cracker.py            # MD5 brute-force cracker (educational)
│   ├── Fibonacci.py          # Fibonacci sequence generator
│   └── vcipher.py            # Vigenere cipher (encrypt / decrypt)
└── tests/                    # Unit tests (stdlib unittest)
    ├── test_cesar.py
    ├── test_cli.py
    ├── test_cracker.py
    ├── test_fibonacci.py
    ├── test_imports.py
    └── test_vcipher.py
```

> The folder `Git Repository` keeps its original name (including the
> space) so existing paths and history are preserved. Run its scripts
> from inside that folder or by full path from the repo root, e.g.
> `python "Git Repository/Cesar_Encrypter.py" --help`.

## Requirements

- Python 3.8+ (developed/tested on 3.11). No packages to install.

## Quick start

```bash
python hello.py
python "Git Repository/Fibonacci.py" 10
python "Git Repository/Cesar_Encrypter.py" encrypt "Hello" --shift 3
python "Git Repository/vcipher.py" encrypt "Hello" --key Hi
python "Git Repository/Cracker.py" --password abc --min-length 1 --max-length 4
```

Each learning script supports `--help`, and importing any module has
**no side effects** — nothing prints and nothing prompts until you call
a function or run the script directly.

## Usage

### Caesar cipher — `Git Repository/Cesar_Encrypter.py`

Shifts ASCII letters by a fixed amount, wrapping the alphabet and
preserving case. Non-ASCII characters and punctuation are unchanged.

```bash
python "Git Repository/Cesar_Encrypter.py" encrypt "Hello" --shift 3   # Khoor
python "Git Repository/Cesar_Encrypter.py" decrypt "Khoor" --shift 3   # Hello
python "Git Repository/Cesar_Encrypter.py" encrypt --shift 3           # prompts
```

```python
from Cesar_Encrypter import encrypt, decrypt  # run from inside "Git Repository"
encrypt("Hello", 3)   # 'Khoor'
decrypt("Khoor", 3)   # 'Hello'
```

### Vigenere cipher — `Git Repository/vcipher.py`

Shifts each letter by a repeating keyword. Case is preserved;
non-letters are unchanged and do not advance the keyword.

```bash
python "Git Repository/vcipher.py" encrypt "Hello" --key Hi   # Omstv
python "Git Repository/vcipher.py" decrypt "Omstv" --key Hi   # Hello
```

```python
from vcipher import generate_key, encrypt, decrypt
generate_key("Hello", "Hi")  # 'HiHiH'
encrypt("Hello", "Hi")       # 'Omstv'
decrypt("Omstv", "Hi")       # 'Hello'
```

### Fibonacci — `Git Repository/Fibonacci.py`

```bash
python "Git Repository/Fibonacci.py" 10
# 0 1 1 2 3 5 8 13 21 34 (one per line, plus timing on stderr)
```

```python
from Fibonacci import calc_fib, fibonacci
calc_fib(7)   # [0, 1, 1, 2, 3, 5, 8]
fibonacci(5)  # [0, 1, 1, 2, 3]
```

### MD5 cracker — `Git Repository/Cracker.py`

> **Educational use only.** MD5 is broken and must never protect real
> passwords. Only test hashes you own or have permission to test.
> Brute force grows exponentially — keep lengths small.

```bash
# Crack a known hash (md5("abc")):
python "Git Repository/Cracker.py" --hash 900150983cd24fb0d6963f7d28e17f72 --min-length 1 --max-length 4

# Demo: hash a password, then crack it back:
python "Git Repository/Cracker.py" --password abc --min-length 1 --max-length 4
```

```python
from Cracker import crack_hash, md5_hexdigest
crack_hash(md5_hexdigest("abc"), 1, 3)  # 'abc'
```

## Tests

```bash
python -m unittest discover -s tests -v
# or, if pytest is installed:
python -m pytest tests -v
```

## What was fixed

- **No import-time side effects:** previously `Cracker.py` prompted for
  input and `Fibonacci.py` printed 500 numbers on import. All modules
  are now import-safe behind `if __name__ == "__main__":` guards.
- **Caesar:** removed debug `print(ord(...))` noise, added alphabet
  wrapping, case preservation, `decrypt()`, and a CLI. `encrypt()`
  still prompts when called with no arguments (legacy behaviour).
- **Cracker:** fixed the alphabet (was missing `j`, `q`, `x`, `z`),
  fixed the circular hash-the-input logic (now cracks a given hash
  directly), fixed the broken `cracker()` (globals, inner-loop-only
  `break`), removed the fragile `from Cesar_Encrypter import *`,
  and added validation plus a CLI.
- **Fibonacci:** removed the shared global list (repeat calls no
  longer corrupt results), removed the unused `math` import and the
  `ciel` typo, `calc_fib()` now *returns* a list instead of only
  printing, and the CLI defaults to 10 numbers instead of 500.
- **Vigenere:** `generate_key()` previously returned a list in one
  branch and `None` in the other and printed on every step. It now
  always returns a string, and full `encrypt()`/`decrypt()` were
  implemented.
- **Hygiene:** docstrings, type hints, `argparse` CLIs, `.gitignore`
  for `__pycache__`/venvs, and a unit-test suite.
