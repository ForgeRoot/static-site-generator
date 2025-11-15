from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
from htmlnode import LeafNode, ParentNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.CODE:
            node = LeafNode("code", text_to_textnodes(block))
        if type == BlockType.QUOTE:
            node = LeafNode("blockquote", block)
        if type == BlockType.UNORDERED_LIST:
            node = ParentNode("ul", text_to_textnodes(block))

        nodes = text_to_textnodes(block)


        