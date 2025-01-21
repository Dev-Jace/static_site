import re

from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode




class TextType(Enum):
    TEXT = "text"
    BOLD = "Bold" 
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Images"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url 

    def __eq__(self, o_TextNode):
        if not isinstance(o_TextNode, TextNode):
            return False
        if self.text == o_TextNode.text:
            if self.text_type == o_TextNode.text_type:
                if self.url == o_TextNode.url:
                    return True
        return False

    def __repr__(self):
        return f"{self.text}, {self.text_type}, {self.url}"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case(TextType.TEXT):
            return LeafNode(tag=None, value=text_node.text)
        case(TextType.BOLD):
            return LeafNode(tag="b",value=text_node.text)
        case(TextType.ITALIC):
            return LeafNode(tag="i",value=text_node.text)
        case(TextType.CODE):
            return LeafNode(tag="code",value=text_node.text)
        case(TextType.LINK):
            return LeafNode(tag="a",value=text_node.text,props={"href":text_node.url,})
        case(TextType.IMAGE):
            return LeafNode(tag="img",value="",props={"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("~Not a valid type~")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #old_nodes is a [] of TextNode
    #delimiter is what we are using to split the old_nodes
    #text_type is what will encapsulate the "delimited" text
    new_nodes = []

    for node in old_nodes:
        
        holder = node.text
        delim_count = 0

        if node.text_type == TextType.TEXT:
            
            while delimiter in holder:
                if delim_count%2 == 0:
                    if len(holder.split(delimiter,1)[0])>0:
                        new_nodes.append( TextNode(holder.split(delimiter,1)[0],TextType.TEXT) )
                elif delim_count%2 == 1:
                    new_nodes.append( TextNode(holder.split(delimiter,1)[0],text_type) )
                
                delim_count += 1
                if  len( holder.split(delimiter,1) ) > 1:
                    holder = holder.split(delimiter,1)[1]

            if len(holder)>0:
                new_nodes.append( TextNode(holder,TextType.TEXT) )
        else:
            new_nodes.append(node)
        
        if delim_count%2 != 0:
            raise Exception("Invalid Markdown syntax:",node)
    
    return new_nodes

def extract_markdown_images(text):
    if type(text) != str:
        raise Exception("Incorrect data type for img data extraction")
    return re.findall(r'!\[(.*?)\]\((.*?)\)',text )

def extract_markdown_links(text):
    if type(text) != str:
        raise Exception("Incorrect data type for URL data extraction")
    return re.findall(r' \[(.*?)\]\((.*?)\)',text )

def split_nodes_image(old_nodes):
    #old_nodes is a [] of TextNode(s)
    new_nodes = []
    
    for node in old_nodes:
        
        if node.text_type == TextType.TEXT and "![" in node.text:
            holder = node.text
            images = extract_markdown_images(holder)
            for i in images:
                sequence = holder.split(f"![{i[0]}]({i[1]})", 1)
                new_nodes.append( TextNode(sequence[0],TextType.TEXT) )
                new_nodes.append( TextNode(i[0],TextType.IMAGE,url=i[1]) )
                holder = sequence[1]     
            if len(holder)> 0 :
                new_nodes.append( TextNode(holder,TextType.TEXT) )
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    #old_nodes is a [] of TextNode(s)
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type == TextType.TEXT and " [" in node.text:
            holder = node.text
            links = extract_markdown_links(holder)
            for i in links:
                sequence = holder.split(f"[{i[0]}]({i[1]})", 1)
                new_nodes.append( TextNode(text=sequence[0],text_type=TextType.TEXT) )
                new_nodes.append( TextNode(text=i[0],text_type=TextType.LINK,url=i[1]) )
                holder = sequence[1]       
            if len(holder)> 0 :
                new_nodes.append( TextNode(holder,TextType.TEXT) )
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT),]
    delimiters = {"Bold":"**", "Italic":"*", "Code":"`",}

    node = split_nodes_image(node)
    node = split_nodes_link(node)
    

    node = split_nodes_delimiter(node,delimiters["Bold"],TextType.BOLD)
    node = split_nodes_delimiter(node,delimiters["Italic"],TextType.ITALIC)
    node = split_nodes_delimiter(node,delimiters["Code"],TextType.CODE)
    
    

    return node

