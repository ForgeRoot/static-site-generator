import unittest
from htmlnode import HTMLNode


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