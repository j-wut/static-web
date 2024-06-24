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
