import re

from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception("Invalid Markdown syntax: missing closing delimiter.")
            temp_nodes = []
            for i, string in enumerate(split_nodes):
                if string:
                    if i % 2 == 0:
                        temp_nodes.append(TextNode(string, TextType.TEXT))
                    else:
                        temp_nodes.append(TextNode(string, text_type))
            new_nodes.extend(temp_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt_text, url in images:
            split = remaining_text.split(f"![{alt_text}]({url})", 1)
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = split[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt_text, url in links:
            split = remaining_text.split(f"[{alt_text}]({url})", 1)
            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            remaining_text = split[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
