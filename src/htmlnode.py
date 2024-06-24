class HTMLNode:
    def __init__(self, tag = None, value = None, children = [], props = {}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return "".join([f' {k}="{v}"' for k,v in self.props.items()])
    def __repr__(self):
        return {"tag": self.tag, "value":self.value, "children": self.children, "props": self.props}

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = {}):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = [], props = {}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode tag must be set")
        if self.children is None:
            raise ValueError("ParentNode children cannot be None")
        return f'<{self.tag}{self.props_to_html()}>{"".join([child.to_html() for child in self.children])}</{self.tag}>'

