import unittest
from pathlib import Path
from greaper.filewalker import get_files_to_search, is_text_file

class TestFilewalker(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with some files for testing
        self.test_dir = Path("test_filewalker_tmp")
        self.test_dir.mkdir(exist_ok=True)
        (self.test_dir / "a.py").write_text("print('hello')\n")
        (self.test_dir / "b.txt").write_text("hello world\n")
        (self.test_dir / "c.bin").write_bytes(b"\x00\x01\x02\x03")
        (self.test_dir / "d.md").write_text("# Markdown\n")
        (self.test_dir / "e.log").write_text("logfile\n")

    def tearDown(self):
        # Clean up test files
        for f in self.test_dir.iterdir():
            f.unlink()
        self.test_dir.rmdir()

    def test_get_files_to_search_default(self):
        files = list(get_files_to_search(path=self.test_dir))
        filenames = {f.name for f in files}
        # Should include .py, .txt, .md, but not .bin (binary)
        self.assertIn("a.py", filenames)
        self.assertIn("b.txt", filenames)
        self.assertIn("d.md", filenames)
        self.assertNotIn("c.bin", filenames)

    def test_include_exclude(self):
        files = list(get_files_to_search(path=self.test_dir, include=["*.py", "*.md"], exclude=["*.md"]))
        filenames = {f.name for f in files}
        self.assertIn("a.py", filenames)
        self.assertNotIn("d.md", filenames)

    def test_is_text_file(self):
        self.assertTrue(is_text_file(self.test_dir / "a.py"))
        self.assertFalse(is_text_file(self.test_dir / "c.bin"))

if __name__ == "__main__":
    unittest.main()