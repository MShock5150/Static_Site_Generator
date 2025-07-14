from blocktype import BlockType
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
from markdown_blocks import markdown_to_blocks, block_to_block_type


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            nodes.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            nodes.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            nodes.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            nodes.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            nodes.append(ul_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            nodes.append(ol_to_html_node(block))
    return ParentNode("div", nodes)


def paragraph_to_html_node(block):
    children = text_to_children(block)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    if level == 0 or level >= len(block) or block[level] != " ":
        raise ValueError("Invalid heading format")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        content = line.lstrip(">").lstrip(" ")
        new_lines.append(content)
    content = "\n".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ul_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        content = line.lstrip("* ").lstrip("- ")
        children = text_to_children(content)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)


def ol_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        index_of_space = line.find(" ")
        content = line[index_of_space + 1 :]
        children = text_to_children(content)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block format")
    stripped_text = block[3:-3].lstrip()
    return ParentNode("pre", [LeafNode("code", stripped_text)])


def text_to_children(text):
    children = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children
