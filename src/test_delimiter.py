import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_single(self):
        node = TextNode(
            "Text before ![alt](url.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url.png"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_at_start(self):
        node = TextNode("![alt](url.png) text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "url.png"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_at_end(self):
        node = TextNode("Text before ![alt](url.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_only(self):
        node = TextNode("![alt](url.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "url.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Just plain text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_non_text_node(self):
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Text with ![image](url.png)", TextType.TEXT),
            TextNode("Italic text", TextType.ITALIC),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Bold text", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url.png"),
                TextNode("Italic text", TextType.ITALIC),
            ],
            new_nodes,
        )
    
    def test_split_images_adjacent(self):
        node = TextNode("![img1](url1.png)![img2](url2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1.png"),
                TextNode("img2", TextType.IMAGE, "url2.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_empty_alt(self):
        node = TextNode("Text ![](url.png) more", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "url.png"),
                TextNode(" more", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
            ],
            new_nodes,
        )
    
    def test_split_links_single(self):
        node = TextNode("Text before [link](url.com) text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_at_start(self):
        node = TextNode("[link](url.com) text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url.com"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_at_end(self):
        node = TextNode("Text before [link](url.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_only(self):
        node = TextNode("[link](url.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Just plain text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_ignores_images(self):
        node = TextNode("Text ![image](img.png) more text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ![image](img.png) more text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_non_text_node(self):
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Text with [link](url.com)", TextType.TEXT),
            TextNode("Code text", TextType.CODE),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Bold text", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
                TextNode("Code text", TextType.CODE),
            ],
            new_nodes,
        )
    
    def test_split_links_adjacent(self):
        node = TextNode("[link1](url1.com)[link2](url2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1.com"),
                TextNode("link2", TextType.LINK, "url2.com"),
            ],
            new_nodes,
        )
    
    def test_split_links_empty_text(self):
        node = TextNode("Text [](url.com) more", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("", TextType.LINK, "url.com"),
                TextNode(" more", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_with_links_present(self):
        node = TextNode(
            "![img](img.png) and [link](url.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "img.png"),
                TextNode(" and [link](url.com)", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_empty_list(self):
        self.assertListEqual([], split_nodes_image([]))
        self.assertListEqual([], split_nodes_link([]))
    
    def test_split_three_images(self):
        node = TextNode(
            "![a](1.png) text ![b](2.png) more ![c](3.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "1.png"),
                TextNode(" text ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "2.png"),
                TextNode(" more ", TextType.TEXT),
                TextNode("c", TextType.IMAGE, "3.png"),
            ],
            new_nodes,
        )
    
class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )
    
    def test_text_to_textnodes_plain(self):
        nodes = text_to_textnodes("Just plain text")
        self.assertListEqual([TextNode("Just plain text", TextType.TEXT)], nodes)

    def test_text_to_textnodes_only_bold(self):
        nodes = text_to_textnodes("**bold**")
        self.assertListEqual([TextNode("bold", TextType.BOLD)], nodes)

    def test_text_to_textnodes_nested_styles(self):
        nodes = text_to_textnodes("**bold**_italic_`code`")
        self.assertListEqual([
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ], nodes)

    def test_text_to_textnodes_image_only(self):
        nodes = text_to_textnodes("![alt](url.png)")
        self.assertListEqual([TextNode("alt", TextType.IMAGE, "url.png")], nodes)

    def test_text_to_textnodes_link_only(self):
        nodes = text_to_textnodes("[text](url.com)")
        self.assertListEqual([TextNode("text", TextType.LINK, "url.com")], nodes)

    def test_text_to_textnodes_all_types_adjacent(self):
        nodes = text_to_textnodes("**b**_i_`c`![img](i.png)[link](l.com)")
        self.assertListEqual([
            TextNode("b", TextType.BOLD),
            TextNode("i", TextType.ITALIC),
            TextNode("c", TextType.CODE),
            TextNode("img", TextType.IMAGE, "i.png"),
            TextNode("link", TextType.LINK, "l.com"),
        ], nodes)

    def test_text_to_textnodes_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([], nodes)

    def test_text_to_textnodes_complex_mix(self):
        nodes = text_to_textnodes(
            "Check out **this _nested_ bold** and `code with spaces` "
            "plus ![image](img.png) and [multiple](url1.com) [links](url2.com)!"
        )

if __name__ == "__main__":
    unittest.main()