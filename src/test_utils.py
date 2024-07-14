import unittest
import utils

from textnode import TextNode

class TestUtils(unittest.TestCase):
    def assert_in_out(self, fn, input, out):
        self.assertEqual(fn(input), out)

    def test_extract_markdown_links(self):
        input = "[link](https://www.example.com) This is text with a [link](https://www.example.com) and [another](https://www.example.com/another) and an ![image](https://www.example.com/image.png)"
        expected = (["", " This is text with a ", " and ", " and an ![image](https://www.example.com/image.png)"], [("link", "https://www.example.com"), ("link", "https://www.example.com"), ("another", "https://www.example.com/another")])
        self.assert_in_out(utils.extract_markdown_links, input, expected)
     
    def test_extract_markdown_links(self):
        input = "![image](https://www.example.com/image.png) This is text with a ![image2](https://www.example.com/image2.png) and ![another](https://www.example.com/another.png) and a [link](https://www.example.com)"
        expected = (["", " This is text with a ", " and ", " and a [link](https://www.example.com)"], [("image", "https://www.example.com/image.png"), ("image2", "https://www.example.com/image2.png"), ("another", "https://www.example.com/another.png")])
        self.assert_in_out(utils.extract_markdown_images, input, expected)

    def test_split_string_to_text_nodes(self):
        input = "**This is a text node**"
        expected_nodes = [TextNode("This is a text node", "bold")]
        self.assert_in_out(utils.split_string_to_text_nodes, input, expected_nodes)

        input = "*italics*"
        expected_nodes = [TextNode("italics", "italics")]
        self.assert_in_out(utils.split_string_to_text_nodes, input, expected_nodes)

        input = "***italics*bold**"
        expected_nodes = [TextNode([TextNode("italics", "italics"),TextNode("bold","text")],"bold")]
        self.assert_in_out(utils.split_string_to_text_nodes, input, expected_nodes)

    def test_split_string_images(self):
        input = "**This is a text node** ![image](https://www.example.com/image.png)"
        expected_nodes = [[TextNode("This is a text node", "bold"), TextNode(" ", "text")], TextNode("image", "image", "https://www.example.com/image.png")]
        self.assert_in_out(utils.split_string_images, input, expected_nodes)

    def test_split_string_links(self):
        input = "*italics* [link](https://www.example.com/)"
        expected_nodes = [[TextNode("italics", "italics"),  TextNode(" ", "text")],  TextNode("link", "link", "https://www.example.com/")]
        self.assert_in_out(utils.split_string_links, input, expected_nodes)

        # input = "***italics*bold**"
        # expected_nodes = [TextNode([TextNode("italics", "italics"),TextNode("bold","text")],"bold")]
        # self.assert_in_out(utils.split_string_to_text_nodes, input, expected_nodes)
        

   


if __name__ == "__main__":
    unittest.main()

