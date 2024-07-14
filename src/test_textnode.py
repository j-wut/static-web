import unittest

from textnode import TextNode
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_to_markdown(self):
        node = TextNode("This is a text node", "bold")
        expected = "**This is a text node**"
        self.assertEqual(node.to_markdown(), expected)
        
        node = TextNode("This is a text node", "italic")
        expected = "*This is a text node*"
        self.assertEqual(node.to_markdown(), expected)

        node = TextNode("This is a text node", "code")
        expected = "`This is a text node`"
        self.assertEqual(node.to_markdown(), expected)

        node = TextNode("link", "link","https://www.example.com")
        expected = "[link](https://www.example.com)"
        self.assertEqual(node.to_markdown(), expected)

        node = TextNode("image", "image","https://www.example.com/image.png")
        expected = "![image](https://www.example.com/image.png)"
        self.assertEqual(node.to_markdown(), expected)

        node = node = TextNode([TextNode("link", "link","https://www.example.com")], "bold")
        expected = "**[link](https://www.example.com)**"
        self.assertEqual(node.to_markdown(), expected)

if __name__ == "__main__":
    unittest.main()
