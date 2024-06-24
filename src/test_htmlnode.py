import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'

    def test_leaf_node_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        assert node1.to_html() == '<p>This is a paragraph of text.</p>'
        assert node2.to_html() == '<a href="https://www.google.com">Click me!</a>'

    def test_parent_node_to_html(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
                )
        assert node.to_html() == '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'


if __name__ == "__main__":
    unittest.main()
