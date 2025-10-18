import unittest
from delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):
    def test_delimiter_single_pair(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
    
    def test_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is plain text", TextType.TEXT),
        ])
    
    def test_delimiter_at_start(self):
        node = TextNode("`code` and text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code", TextType.CODE),
            TextNode(" and text", TextType.TEXT),
        ])
    
    def test_delimiter_at_end(self):
        node = TextNode("text and `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("text and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])
    
    def test_delimiter_empty_middle(self):
        node = TextNode("text `` more", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("text ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" more", TextType.TEXT),
        ])
    
    def test_multiple_pairs(self):
        node = TextNode("This `code1` and `code2` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])
    
    def test_mixed_node_types(self):
        nodes = [
            TextNode("Normal `code` text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More `code` here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("Normal ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),  # Unchanged
            TextNode("More ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])
    
    def test_different_delimiter_underscore(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])
    
    def test_multi_char_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])
    
    def test_unbalanced_delimiter_raises(self):
        node = TextNode("This has `unclosed code", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("missing closing delimiter", str(context.exception))
    
    def test_adjacent_pairs(self):
        node = TextNode("text`code1``code2`end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("text", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
            TextNode("end", TextType.TEXT),
        ])
    
    def test_whitespace_preserved(self):
        node = TextNode("  `  code  `  ", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("  ", TextType.TEXT),
            TextNode("  code  ", TextType.CODE),
            TextNode("  ", TextType.TEXT),
        ])
    
    def test_only_delimiter(self):
        node = TextNode("`code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code", TextType.CODE),
        ])
    
    def test_three_pairs(self):
        node = TextNode("`a` `b` `c`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("a", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("c", TextType.CODE),
        ])
    
    def test_empty_input_list(self):
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])


if __name__ == "__main__":
    unittest.main()