import re
from blocktype import BlockType


def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split("\n")
    current_block = []
    for line in lines:
        if line.strip():
            current_block.append(line)
        else:
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
    if current_block:
        blocks.append("\n".join(current_block))
    return blocks


def block_to_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    lines = markdown.split("\n")
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    is_star_list = True
    for line in lines:
        if not line.startswith("* "):
            is_star_list = False
            break
    if is_star_list:
        return BlockType.UNORDERED_LIST
    is_dash_list = True
    for line in lines:
        if not line.startswith("- "):
            is_dash_list = False
            break
    if is_dash_list:
        return BlockType.UNORDERED_LIST
    is_ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
