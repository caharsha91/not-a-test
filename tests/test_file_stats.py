import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]


def run_cli(content: str) -> tuple[int, str, str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir) / "sample.txt"
        target.write_text(content, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "file_stats.py", str(target)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


class FileStatsCLITests(unittest.TestCase):
    def test_counts_basic(self):
        code, stdout, stderr = run_cli("Hello world\nSecond line")

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Characters: 23", stdout)
        self.assertIn("Lines: 2", stdout)
        self.assertIn("Spaces: 2", stdout)
        self.assertIn("Tabs: 0", stdout)
        self.assertIn("Words: 4", stdout)
        self.assertIn("Special characters: 0", stdout)

    def test_counts_special_characters(self):
        code, stdout, stderr = run_cli("123 !@\n\tNext")

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Characters: 12", stdout)
        self.assertIn("Lines: 2", stdout)
        self.assertIn("Spaces: 1", stdout)
        self.assertIn("Tabs: 1", stdout)
        self.assertIn("Words: 2", stdout)
        self.assertIn("Special characters: 2", stdout)

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing = Path(tmp_dir) / "missing.txt"
            result = subprocess.run(
                [sys.executable, "file_stats.py", str(missing)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("error:", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
