import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        # Tests a simple case with one child
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        # Tests rendering with several children
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_grandchildren(self):
        # Tests that recursion works correctly with nested ParentNodes
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        # Tests that the parent's props are rendered correctly
        node = ParentNode(
            "div",
            [LeafNode("p", "I am a child")],
            {"class": "container", "id": "main-content"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main-content"><p>I am a child</p></div>',
        )

    def test_to_html_deeply_nested(self):
        # Tests multiple levels of nesting
        node = ParentNode(
            "main",
            [
                ParentNode(
                    "div",
                    [
                        LeafNode("p", "Paragraph 1"),
                        ParentNode("div", [LeafNode("p", "Deeply nested paragraph")]),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<main><div><p>Paragraph 1</p><div><p>Deeply nested paragraph</p></div></div></main>",
        )

    def test_error_no_tag(self):
        # Tests that a ValueError is raised if the tag is missing
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("p", "child")])
            node.to_html()

    def test_error_no_children(self):
        # Tests that a ValueError is raised if children are missing
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()


if __name__ == "__main__":
    unittest.main()
