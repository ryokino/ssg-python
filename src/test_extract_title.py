import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_leading_trailing_whitespace(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_title_with_other_content(self):
        md = """# My Title

Some paragraph text here.

## A subtitle
"""
        self.assertEqual(extract_title(md), "My Title")

    def test_title_not_first_line(self):
        md = """Some intro text

# The Real Title

More content
"""
        self.assertEqual(extract_title(md), "The Real Title")

    def test_no_h1_raises_exception(self):
        with self.assertRaises(Exception):
            extract_title("## Not an h1\n\n### Also not an h1")

    def test_no_h1_empty_string_raises_exception(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_h2_is_not_h1(self):
        with self.assertRaises(Exception):
            extract_title("## This is h2")

    def test_h1_with_inline_markdown(self):
        self.assertEqual(extract_title("# Hello **world**"), "Hello **world**")


if __name__ == "__main__":
    unittest.main()
