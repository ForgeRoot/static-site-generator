import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("h1", "title")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "title")
    
    def test_init_ul(self):
        children = HTMLNode("li", "Item1")
        node = HTMLNode("ul", None, children)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("a", None, None,{"href": "https://www.google.com", "target": "_blank"} )
        self.assertEqual(
            "HTMLNode(a, None, children: None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node)
        )

    def test_props_to_html(self):
        node = HTMLNode("a", None, None,{"href": "https://www.google.com", "target": "_blank"} )
        self.assertEqual(
            node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\""
        )
    
    def test_props_to_html_none(self):
        node = HTMLNode("p", "text", None, None)
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_p_to_html(self):
        p = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(p.to_html(), "<p>This is a paragraph of text.</p>")

    def test_h1_to_html(self):
        h1 = LeafNode("h1", "This is a title of text.")
        self.assertEqual(h1.to_html(), "<h1>This is a title of text.</h1>")

    def test_a_to_html(self):
        a = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(a.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode("div", [
            LeafNode("p", "First"),
            LeafNode("p", "Second"),
            LeafNode("p", "Third")
        ])
        self.assertEqual(
            node.to_html(),
            "<div><p>First</p><p>Second</p><p>Third</p></div>"
        )

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "test")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )