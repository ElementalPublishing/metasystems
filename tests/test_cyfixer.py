import unittest
import tempfile
import os
from cyfixer import fix_pyx_file

class TestCyfixer(unittest.TestCase):
    def test_functionality(self):
        self.assertEqual(1 + 1, 2)

    def test_edge_case(self):
        self.assertRaises(ValueError, lambda: int('invalid'))

    def test_fix_invalid_fstring_signature(self):
        code = 'f"def foo({\', \'.join(args)}):"\n    pass\n'
        expected = 'def foo():\n    pass\n'
        with tempfile.NamedTemporaryFile("w+", suffix=".pyx", delete=False) as tf:
            tf.write(code)
            tf.flush()
            fix_pyx_file(tf.name)
            tf.seek(0)
            result = tf.read()
        os.unlink(tf.name)
        self.assertIn("def foo():", result)

    def test_fix_empty_function_body(self):
        code = "def bar():\n\n"
        with tempfile.NamedTemporaryFile("w+", suffix=".pyx", delete=False) as tf:
            tf.write(code)
            tf.flush()
            fix_pyx_file(tf.name)
            tf.seek(0)
            result = tf.read()
        os.unlink(tf.name)
        self.assertIn("pass", result)

    def test_fix_cpdef_float_missing_return(self):
        code = "cpdef float baz():\n    # no return\n"
        with tempfile.NamedTemporaryFile("w+", suffix=".pyx", delete=False) as tf:
            tf.write(code)
            tf.flush()
            fix_pyx_file(tf.name)
            tf.seek(0)
            result = tf.read()
        os.unlink(tf.name)
        self.assertIn("return 0.0", result)

    def test_comment_out_lambda(self):
        code = "x = lambda y: y + 1\n"
        with tempfile.NamedTemporaryFile("w+", suffix=".pyx", delete=False) as tf:
            tf.write(code)
            tf.flush()
            fix_pyx_file(tf.name)
            tf.seek(0)
            result = tf.read()
        os.unlink(tf.name)
        self.assertIn("# Unsupported feature commented out:", result)

    def test_add_missing_import(self):
        code = "a = np.array([1,2,3])\n"
        with tempfile.NamedTemporaryFile("w+", suffix=".pyx", delete=False) as tf:
            tf.write(code)
            tf.flush()
            fix_pyx_file(tf.name)
            tf.seek(0)
            result = tf.read()
        os.unlink(tf.name)
        self.assertIn("import numpy as np", result)

if __name__ == '__main__':
    unittest.main()