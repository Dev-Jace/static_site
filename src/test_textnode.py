import unittest

from textnode import *
from markdown_blocks import block_to_block_type, markdown_to_blocks


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertEqual(node.text_type, node2.text_type)

    def test_url(self):
         node = TextNode("This is a text node", TextType.BOLD)
         #node2 = TextNode("This is not a text node", TextType.BOLD)
         self.assertIsNone(node.url)

class TestConverter(unittest.TestCase):
    def test_WrongType(self):
        with self.assertRaises(Exception):
            txt_node = TextNode("wrong type",TextType.weird,url= "google.com")
            text_node_to_html_node(txt_node)

    def test_conversion_N(self):
        result = LeafNode(tag=None,value="normal leaf")
        txt_node = TextNode("normal leaf",TextType.TEXT)
        conv_node = text_node_to_html_node(txt_node)
        self.assertEqual(result,conv_node)
    
    def test_conversion_B(self):
        result = LeafNode(tag="b",value="bold leaf")
        txt_node = text_node_to_html_node(TextNode("bold leaf",TextType.BOLD) )
        self.assertEqual(result,txt_node)

    def test_conversion_I(self):
        result = LeafNode(tag="i",value="italic leaf")
        txt_node = text_node_to_html_node(TextNode("italic leaf",TextType.ITALIC) )
        self.assertEqual(result,txt_node)

    def test_conversion_CODE(self):
        result = LeafNode(tag="code",value="code leaf")
        txt_node = text_node_to_html_node(TextNode("code leaf",TextType.CODE) )
        self.assertEqual(result,txt_node)

    def test_conversion_Link(self):
        result = LeafNode(tag="a",value="link leaf",props={"href":"google.com",})
        txt_node = text_node_to_html_node(TextNode("link leaf",TextType.LINK,url="google.com") )
        self.assertEqual(result,txt_node)

    def test_conversion_IMG(self):
        result = LeafNode(tag="img",value="", props={"src":"google.com/image","alt":"image leaf"})
        txt_node = text_node_to_html_node( TextNode("image leaf",TextType.IMAGE,url="google.com/image") )
        self.assertEqual(result,txt_node)    
    
class TestSplitNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
        input = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, input)

    def test_WrongType(self):
        with self.assertRaises(Exception):
            node = TextNode("wrong type",TextType.weird,url= "google.com")
            input = split_nodes_delimiter([node], "`", TextType.bob)
            text_node_to_html_node(input)

class TestExtractNodes(unittest.TestCase):
    #Image
    def test_eq(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        input = extract_markdown_images(text)
        self.assertEqual(result, input)

    def test_WrongType(self):
        with self.assertRaises(Exception):
            text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            extract_markdown_images(text)

    def test_WrongType(self):
        with self.assertRaises(Exception):
            text = []
            extract_markdown_images(text)
    
    #URL
    def test_eq(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        input = extract_markdown_links(text)
        self.assertEqual(result, input)

    def test_WrongType(self):
        with self.assertRaises(Exception):
            text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            extract_markdown_links(text)

    def test_WrongType(self):
        with self.assertRaises(Exception):
            text = []
            extract_markdown_links(text)

class TestImageSplit(unittest.TestCase):
    def test_eq(self):
        node = TextNode(
    text="This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
    text_type=TextType.TEXT,
)
        result = [
                    TextNode(text="This is text with a link ", text_type=TextType.TEXT),
                    TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
                ]
        new_nodes = split_nodes_image([node])
        self.assertEqual(result, new_nodes)

class TestLinkSplit(unittest.TestCase):
    def test_eq(self):
        node = TextNode(
    text="This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    text_type=TextType.TEXT,
)
        result = [
                    TextNode(text="This is text with a link ", text_type=TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                ]
        new_nodes = split_nodes_link([node])
        self.assertEqual(result, new_nodes)

#37

class TestTEXT_to_TextNodes(unittest.TestCase):
    def test_eq(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        test_node = TextNode(text,TextType.TEXT)
        result = [
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
                ]
        answer = text_to_textnodes(text)

        self.assertEqual(answer, result)

class TestMarkdown_to_Blocks(unittest.TestCase):
    def test_eq(self):
        result = ["# This is a heading", 
                  "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
                  """* This is the first list item in a list block
* This is a list item
* This is another list item""" 
                ]
        input = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        answer = markdown_to_blocks(input)
        self.assertEqual(answer, result)

    def test_triple_enter(self):
        result = ["""This 
is 
a 
set.""","End"]
        input = """This 
is 
a 
set.

End"""


        answer = markdown_to_blocks(input)
        self.assertEqual(answer, result)

class TestMarkdown_to_Blocks(unittest.TestCase):
    def test_eq(self):
        result = ["heading-1", 
                  "heading-2", 
                  "paragraph", 
                  "unordered list", 
                  "unordered list", 
                  "ordered list"]
        input = ["# This is a heading",
                  "## This is a heading",
                  "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", 
                  """* This is the first list item in a list block
* This is a list item
* This is another list item""", 
"""- This is the first list item in a list block
- This is a list item
- This is another list item""" ,
"""1. This
2. is
3. ordered"""]
        answer = list(map(block_to_block_type, input) )

        self.assertEqual(result, answer)




if __name__ == "__main__":
    unittest.main()
