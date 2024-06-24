import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'

    def test_leaf_node_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        assert node1.to_html() == '<p>This is a paragraph of text.</p>'
        assert node2.to_html() == '<a href="https://www.google.com">Click me!</a>'

if __name__ == "__main__":
    unittest.main()
