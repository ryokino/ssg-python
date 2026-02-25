from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType
from text_to_textnodes import text_to_textnodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        block_nodes.append(html_node)
    return ParentNode("div", block_nodes)


def block_to_html_node(block, block_type):
    if block_type == BlockType.heading:
        return heading_to_html_node(block)
    if block_type == BlockType.code:
        return code_to_html_node(block)
    if block_type == BlockType.quote:
        return quote_to_html_node(block)
    if block_type == BlockType.unordered_list:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ordered_list:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.paragraph:
        return paragraph_to_html_node(block)
    raise ValueError(f"Unknown block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    # Strip the opening and closing ```
    text = block[3:-3].strip("\n")
    # Add trailing newline for code blocks
    text = text + "\n"
    # Code blocks should NOT do inline markdown parsing
    text_node = TextNode(text, TextType.TEXT)
    code_leaf = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [code_leaf])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        # Remove the leading '>' and optional space
        stripped_lines.append(line.lstrip(">").strip())
    text = " ".join(stripped_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        # Remove the leading "- "
        text = line[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        # Remove the leading "N. " (number followed by ". ")
        dot_index = line.index(". ")
        text = line[dot_index + 2 :]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", children)
