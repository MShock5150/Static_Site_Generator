import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from main import text_node_to_html_node


class TestMain(unittest.TestCase):
    def test_text_node_to_html_text(self):
        # Tests a basic TEXT type node
        text_node = TextNode("This is raw text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is raw text")

    def test_text_node_to_html_bold(self):
        # Tests a BOLD type node
        text_node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_text_node_to_html_italic(self):
        # Tests an ITALIC type node
        text_node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_text_node_to_html_code(self):
        # Tests a CODE type node
        text_node = TextNode("self.assertEqual()", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "self.assertEqual()")

    def test_text_node_to_html_link(self):
        # Tests a LINK type node
        text_node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_text_node_to_html_image(self):
        # Tests an IMAGE type node
        text_node = TextNode(
            "An image", TextType.IMAGE, "https://example.com/image.png"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.png", "alt": "An image"}
        )

    def test_invalid_text_type_raises_error(self):
        # Tests that an invalid TextType raises an exception
        text_node = TextNode("Some text", "invalid_type")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
