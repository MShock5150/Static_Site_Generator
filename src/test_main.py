import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode

# Make sure your functions are in a file that can be imported, like 'main.py'
# or another utility file.
from main import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestMain(unittest.TestCase):
    # ######################################
    # ## Tests for text_node_to_html_node ##
    # ######################################

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

    # ##########################################
    # ## Tests for split_nodes_delimiter      ##
    # ##########################################

    def test_split_nodes_standard(self):
        """
        Tests a standard case with one code block in the middle.
        """
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_multiple_delimiters(self):
        """
        Tests splitting a node with multiple delimited sections.
        """
        node = TextNode("A `code` word and another `code` word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("A ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word and another ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" word.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_start(self):
        """
        Tests a case where the delimiter is at the beginning of the string.
        """
        node = TextNode("*bold word* at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected_nodes = [
            TextNode("bold word", TextType.BOLD),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_end(self):
        """
        Tests a case where the delimiter is at the end of the string.
        """
        node = TextNode("Text at the start *bold word*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected_nodes = [
            TextNode("Text at the start ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_non_text_node_passed_through(self):
        """
        Tests that a non-text node is passed through unchanged.
        """
        node = TextNode("This is a bold node", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is a bold node", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_unclosed_delimiter_raises_error(self):
        """
        Tests that an unclosed delimiter raises an exception.
        """
        node = TextNode("This has an *unclosed bold block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "*", TextType.BOLD)

    # #############################################
    # ## Tests for extract_markdown_images/links ##
    # #############################################

    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "second image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
        )

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
        )

    def test_no_matches(self):
        text = "This is plain text with no images or links."
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_mixed_content(self):
        text = "Here is an ![image](image.png) and a [link](link.com)."
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertEqual(image_matches, [("image", "image.png")])
        self.assertEqual(link_matches, [("link", "link.com")])

    # #################################
    # ## Tests for split_nodes_image ##
    # #################################

    def test_split_image_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and some text", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )

    # ################################
    # ## Tests for split_nodes_link ##
    # ################################

    def test_split_link_single(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    def test_split_link_multiple(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://www.example.com/another"),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "Some text and a [link](https://www.example.com)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Some text and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )

    # ################################
    # ## Test for text_to_textnodes ##
    # ################################

    def test_text_to_textnodes_all_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()
