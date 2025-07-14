import unittest

# Assuming your new functions are in 'html_conversion.py'
from html_conversion import markdown_to_html_node


class TestMarkdownToHTMLConversion(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is a paragraph.

This is another paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div><p>This is a paragraph.</p><p>This is another paragraph.</p></div>"
        )
        self.assertEqual(html, expected)

    def test_lists(self):
        md = """
- This is a list
- with items

1. This is an
2. ordered list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>This is a list</li><li>with items</li></ul><ol><li>This is an</li><li>ordered list</li></ol></div>"
        self.assertEqual(html, expected)

    def test_headings(self):
        md = """
# Heading 1

## Heading 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2></div>"
        self.assertEqual(html, expected)

    def test_blockquote(self):
        md = """
> This is a
> blockquote.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a\nblockquote.</blockquote></div>"
        self.assertEqual(html, expected)

    def test_code_block(self):
        md = """
```
# some code here
print("hello")
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            '<div><pre><code># some code here\nprint("hello")\n</code></pre></div>'
        )
        self.assertEqual(html, expected)

    def test_full_document(self):
        md = """
# Welcome to my blog

This is a paragraph with **bold** and _italic_ text.

* List item 1
* List item 2 with `code`

> This is a quote.

And another paragraph with a [link](https://example.com) and an ![image](image.png).
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><h1>Welcome to my blog</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><ul><li>List item 1</li><li>List item 2 with <code>code</code></li></ul><blockquote>This is a quote.</blockquote><p>And another paragraph with a <a href="https://example.com">link</a> and an <img src="image.png" alt="image"></img>.</p></div>'
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
