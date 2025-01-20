

class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #HTML tag
        self.value = value #string in tag
        self.children = children #HTMLNode in this node
        self.props = props #tag attributes, dictionary, 

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props != None:
            props_str = ""
            for prop in self.props:
                props_str += f' {prop}="{self.props[prop]}"'
            return props_str
        return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    def __eq__(self, o_HTMLNode):
        if not isinstance(o_HTMLNode, HTMLNode):
            return False
        if self.tag == o_HTMLNode.tag:
            if self.value == o_HTMLNode.value:
                if self.children == o_HTMLNode.children:
                    if self.props == o_HTMLNode.props:
                        return True
        return False
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        rtn_str = ""
        if type(self.value) != str:
            raise ValueError
        if self.tag != None:
            if self.props != None:
                rtn_str += f"<{self.tag}{self.props_to_html()}>"
            else:
                rtn_str += f"<{self.tag}>"
        rtn_str += self.value
        if self.tag != None:
            rtn_str += f"</{self.tag}>"
        return rtn_str


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__( tag, None, children, props)

    def to_html(self):
        rtn_str = ""
        if type(self.tag) != str:
            self.__repr__()
            raise Exception("Tag invalid")
        if self.children == None:
            raise Exception("children invalid")
        rtn_str += f'<{self.tag}>'
        for child in self.children:
            rtn_str += child.to_html()
        rtn_str += f'</{self.tag}>'
        return rtn_str