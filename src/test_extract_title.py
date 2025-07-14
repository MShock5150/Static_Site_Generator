import unittest

# Assuming your function is in a file named 'extract_title.py'
from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_standard_h1(self):
        """
        Tests a standard case where an h1 is the first line.
        """
        markdown = """
# This is the Title

This is some paragraph text.
"""
        title = extract_title(markdown)
        self.assertEqual(title, "This is the Title")

    def test_no_h1_raises_error(self):
        """
        Tests that an exception is raised if no h1 header is found.
        """
        markdown = """
This is a document
with no h1 header.
## This is an h2
"""
        # The 'with self.assertRaises(...)' block checks that the expected
        # error is raised. The test passes only if the error occurs.
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h1_not_at_start(self):
        """
        Tests that the function finds the h1 even if it's not the first line.
        """
        markdown = """
Some introductory text.

# The Real Title

More text.
"""
        title = extract_title(markdown)
        self.assertEqual(title, "The Real Title")

    def test_other_headings_not_h1(self):
        """
        Tests that other heading levels are correctly ignored.
        """
        markdown = "## Not the title\n### Also not the title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_no_space_after_hash(self):
        """
        Tests that a '#' not followed by a space is not a heading.
        """
        markdown = "#NotATitle\nSome text here."
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
