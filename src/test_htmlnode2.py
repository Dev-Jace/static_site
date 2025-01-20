import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTML_Node(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="a", value="this is the info of value", props={
    "href": "https://www.google.com", 
    "target": "_blank",
})
        node2 = HTMLNode(tag="a", value="this is the info of value", props={
    "href": "https://www.google.com", 
    "target": "_blank",
})
        self.assertEqual(node, node2)

    def test_type(self):
        node = HTMLNode(tag="a", value="this is the info of value")
        node2 = HTMLNode(tag="a", value="this is not the info of value")
        self.assertEqual(node.tag, node2.tag)

    def test_url(self):
         node = HTMLNode()
         #node2 = TextNode("This is not a text node", TextType.BOLD)
         self.assertIsNone(node.tag)

    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="this is the info of value", props={
    "href": "https://www.google.com", 
    "target": "_blank",
})
        self.assertIs(str,type(node.props_to_html()))


#4    
class TestLEAF_Node(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(tag="a", value="this is the info of value", props={
    "href": "https://www.google.com", 
    "target": "_blank",
})
        node2 = LeafNode(tag="a", value="this is the info of value", props={
    "href": "https://www.google.com", 
    "target": "_blank",
})
        self.assertEqual(node, node2)

    def test_eq_(self):
        node = HTMLNode(tag="a", value="this is the info of value", props={
    "href": "https://www.google.com", 
    "target": "_blank",
})
        node2 = LeafNode(tag="a", value="this is the info of value", props={
    "href": "https://www.google.com", 
    "target": "_blank",
})
        self.assertEqual(node, node2)

    def test_children(self):
        node = LeafNode(tag="a", value="this is the info of value")
        self.assertIsNone(node.children)
    
    def test_valError_None(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="a", value=None)
            node.to_html()
    
    def test_valError_List(self):
        with self.assertRaises(ValueError):
            node2 = LeafNode(tag="a", value=[1,2])
            node2.to_html()
    
    def test_valError_dict(self):
        with self.assertRaises(ValueError):
            node3 = LeafNode(tag="a", value={"a":3})
            node3.to_html()
    
    def test_toHTML_Wprops(self):
        node8 = LeafNode(tag="a", value="this is the info of value", props={"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">this is the info of value</a>',
              node8.to_html())

    def test_toHTML_Nprops(self):
        node = LeafNode(tag="a", value="this is the info of value")
        self.assertEqual("<a>this is the info of value</a>", node.to_html())

#12
class TestParent_Node(unittest.TestCase):
    def test_eq(self):
        L_node = LeafNode(tag="a", value="this is the info of value")
        L_node2 = LeafNode(tag="a", value="this is the info of value")
        P_node = ParentNode(tag="a", children=[L_node,L_node2])
        P_node2 = ParentNode(tag="a", children=[L_node,L_node2])
        self.assertEqual(P_node, P_node2)

    def test_output(self):
        result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        T_node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        self.assertEqual(result, T_node.to_html())

    def test_nesting(self):
        result = "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>"
        T_node = ParentNode("p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),],)
        T_node2 = ParentNode("p",
        [
        T_node,
        T_node,
        ],)
        self.assertEqual(result, T_node2.to_html())

#37


if __name__ == "__main__":
    unittest.main()
