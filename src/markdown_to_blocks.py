from enum import Enum


class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def block_to_block_type(block):
    # Heading: 1-6 # characters followed by a space
    if block.startswith("#"):
        for i in range(1, 7):
            if block.startswith("#" * i + " "):
                return BlockType.heading
        # 7+ # or no space after # → paragraph

    # Code: starts with ``` and newline, ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code

    # Quote: every line must start with >
    lines = block.split("\n")
    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.quote

    # Unordered list: every line must start with "- "
    if block.startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockType.unordered_list

    # Ordered list: lines must start with "1. ", "2. ", "3. ", ...
    if block.startswith("1. "):
        is_ordered = True
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ordered_list

    return BlockType.paragraph


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks
