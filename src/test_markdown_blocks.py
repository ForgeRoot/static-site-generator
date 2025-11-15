import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)



class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        """Test basic markdown splitting with various inline formatting"""
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
    
    def test_heading_paragraph_list(self):
        """Test the example from the instructions"""
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )
    
    def test_excessive_newlines(self):
        """Test that excessive newlines create empty blocks that get filtered out"""
        md = """First block


Second block



Third block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )
    
    def test_leading_and_trailing_whitespace(self):
        """Test that leading and trailing whitespace is stripped from blocks"""
        md = """
   First block with spaces   

  Second block with tabs	

Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with spaces",
                "Second block with tabs",
                "Third block",
            ],
        )
    
    def test_single_block(self):
        """Test with a single block (no double newlines)"""
        md = "Just a single paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph"])
    
    def test_empty_string(self):
        """Test with an empty string"""
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_only_whitespace(self):
        """Test with only whitespace and newlines"""
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_code_block(self):
        """Test with a code block"""
        md = """Here's some code:

```python
def hello():
    print("world")
```

And here's a paragraph after."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here's some code:",
                '```python\ndef hello():\n    print("world")\n```',
                "And here's a paragraph after.",
            ],
        )
    
    def test_multiple_headings(self):
        """Test with multiple heading levels"""
        md = """# Heading 1

## Heading 2

### Heading 3

Regular paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "## Heading 2",
                "### Heading 3",
                "Regular paragraph",
            ],
        )
    
    def test_ordered_list(self):
        """Test with ordered lists"""
        md = """1. First item
2. Second item
3. Third item

Next paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "1. First item\n2. Second item\n3. Third item",
                "Next paragraph",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a simple paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_h1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_h6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_invalid_no_space(self):
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_invalid_too_many(self):
        block = "####### Too many"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote_single_line(self):
        block = ">This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_multi_line(self):
        block = ">Line 1\n>Line 2\n>Line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_unordered_list_dash(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_wrong_order(self):
        block = "1. First\n3. Wrong\n2. Order"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_multiline_paragraph(self):
        block = "This is line 1\nThis is line 2\nThis is line 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()