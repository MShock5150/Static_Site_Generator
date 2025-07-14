import unittest
from blocktype import BlockType
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading(self):
        # Tests standard headings of different levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_not_heading_too_many_hashes(self):
        # A heading cannot have more than 6 hashes
        self.assertEqual(
            block_to_block_type("####### Not a Heading"), BlockType.PARAGRAPH
        )

    def test_code_block(self):
        # Tests a standard code block
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

    def test_not_code_block_unclosed(self):
        # An unclosed code block is just a paragraph
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        # Tests a standard quote block
        self.assertEqual(
            block_to_block_type("> quote\n> another line"), BlockType.QUOTE
        )

    def test_not_quote_block_mixed(self):
        # If not all lines start with '>', it's a paragraph
        self.assertEqual(
            block_to_block_type("> quote\nThis is not a quote"), BlockType.PARAGRAPH
        )

    def test_unordered_list(self):
        # Tests both '*' and '-' as list delimiters
        self.assertEqual(
            block_to_block_type("* item 1\n* item 2"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST
        )

    def test_not_unordered_list_mixed(self):
        # A mix of list delimiters is not a valid list
        self.assertEqual(block_to_block_type("* item 1\n- item 2"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Tests a standard, correctly numbered ordered list
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST
        )

    def test_not_ordered_list_wrong_start(self):
        # An ordered list must start with '1.'
        self.assertEqual(
            block_to_block_type("2. first\n3. second"), BlockType.PARAGRAPH
        )

    def test_not_ordered_list_skipped_number(self):
        # An ordered list must increment by 1 each time
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        # Tests a standard paragraph
        self.assertEqual(
            block_to_block_type("This is just a standard paragraph."),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("This is a\nmultiline paragraph."), BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()
