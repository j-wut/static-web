import unittest
import utils

from textnode import TextNode

class TestUtils(unittest.TestCase):
    def assert_in_out(self, fn, input, out):
        self.assertEqual(fn(input), out)

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


if __name__ == "__main__":
    unittest.main()

