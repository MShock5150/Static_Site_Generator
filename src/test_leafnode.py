import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_basic(self):
        # Tests a simple paragraph tag
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        # Tests rendering with HTML attributes (props)
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_no_tag(self):
        # Tests rendering with no tag, which should return raw text
        node = LeafNode(None, "This is plain text.")
        self.assertEqual(node.to_html(), "This is plain text.")

    def test_to_html_no_value_raises_error(self):
        # Tests that a ValueError is raised if no value is provided
        # The `with self.assertRaises(...)` block is the standard way
        # to test for expected errors. The test passes only if the
        # specified error is raised inside the block.
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()


if __name__ == "__main__":
    unittest.main()
