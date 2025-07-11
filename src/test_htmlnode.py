import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_basic(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        expected_string = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_string)

    def test_props_to_html_none(self):
        node = HTMLNode()
        expected_string = ""
        self.assertEqual(node.props_to_html(), expected_string)

    def test_props_to_html_one(self):
        node = HTMLNode(
            props={
                "href": "https://boot.dev",
            }
        )
        expected_string = ' href="https://boot.dev"'
        self.assertEqual(node.props_to_html(), expected_string)
