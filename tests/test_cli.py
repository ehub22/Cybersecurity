"""Smoke tests for command-line entry points."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "Git Repository"


def run_script(script, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class CommandLineTests(unittest.TestCase):
    def test_caesar_cli(self):
        result = run_script("Cesar_Encrypter.py", "encrypt", "Hello", "--shift", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "Khoor")

    def test_vigenere_cli(self):
        result = run_script("vcipher.py", "encrypt", "Hello", "--key", "Hi")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "Omstv")

    def test_fibonacci_cli_supports_positional_and_named_count(self):
        for args in (("5",), ("--count", "5")):
            with self.subTest(args=args):
                result = run_script("Fibonacci.py", *args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.splitlines(), ["0", "1", "1", "2", "3"])
                self.assertIn("Elapsed time:", result.stderr)

    def test_cracker_cli(self):
        result = run_script(
            "Cracker.py",
            "--hash",
            "0cc175b9c0f1b6a831c399e269772661",
            "--min-length",
            "1",
            "--max-length",
            "1",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Password found: a", result.stdout)


if __name__ == "__main__":
    unittest.main()
