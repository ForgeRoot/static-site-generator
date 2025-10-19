import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

class TestMarkdownExtractor(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_multiple_images(self):
        text = "![first](url1.png) and ![second](url2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("first", "url1.png"),
            ("second", "url2.jpg")
        ], matches)
    
    def test_extract_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)
    
    def test_extract_images_with_spaces(self):
        matches = extract_markdown_images("![alt text](https://example.com/my image.png)")
        self.assertListEqual([("alt text", "https://example.com/my image.png")], matches)
    
    def test_extract_no_images(self):
        matches = extract_markdown_images("Just plain text with no images")
        self.assertListEqual([], matches)
    
    def test_extract_images_ignores_links(self):
        text = "A [link](url.com) and an ![image](img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "img.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)
    
    def test_extract_multiple_links(self):
        text = "[first](url1.com) and [second](url2.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("first", "url1.com"),
            ("second", "url2.com")
        ], matches)
    
    def test_extract_links_empty_text(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)
    
    def test_extract_links_ignores_images(self):
        text = "A ![image](img.png) and a [link](url.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "url.com")], matches)
    
    def test_extract_no_links(self):
        matches = extract_markdown_links("Just plain text")
        self.assertListEqual([], matches)
    
    def test_extract_links_with_spaces(self):
        matches = extract_markdown_links("[click here](https://example.com/my page)")
        self.assertListEqual([("click here", "https://example.com/my page")], matches)
    
    def test_extract_both_images_and_links(self):
        text = "Check out ![pic](img.png) and [visit](site.com)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual([("pic", "img.png")], images)
        self.assertListEqual([("visit", "site.com")], links)
    
    def test_extract_adjacent_markdown(self):
        text = "![img1](url1.png)![img2](url2.png)[link1](site1.com)[link2](site2.com)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual([
            ("img1", "url1.png"),
            ("img2", "url2.png")
        ], images)
        self.assertListEqual([
            ("link1", "site1.com"),
            ("link2", "site2.com")
        ], links)
    
    def test_extract_nested_brackets_not_matched(self):
        text = "![[nested]](url.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_image_before_link(self):
        text = "![alt](img.png)[text](url.com)"
        
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual([("alt", "img.png")], images)
        self.assertListEqual([("text", "url.com")], links)

if __name__ == "__main__":
    unittest.main()