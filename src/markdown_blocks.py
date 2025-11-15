from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            cleaned_blocks.append(stripped_block)
    
    return cleaned_blocks   

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")

    is_code = len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```"
    if is_code:
        return BlockType.CODE

    is_quote = all(line.startswith(">") for line in lines)
    if is_quote:
        return BlockType.QUOTE

    is_unordered_list = all(line.startswith("- ") for line in lines)
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    is_ordered_list = all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines))
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    line0 = lines[0]
    if line0.startswith("#"):
        count = 0
        while count < len(line0) and line0[count] == "#":
            count += 1
        if 1 <= count <= 6 and count < len(line0) and line0[count] == " ":
            return BlockType.HEADING

    return BlockType.PARAGRAPH
