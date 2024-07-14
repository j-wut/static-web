class TextNode:
    def __init__(self,text,text_type,url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return type(self) == type(other) \
                and self.text == other.text \
                and self.text_type == other.text_type \
                and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_markdown(self):
        selftext= self.text if type(self.text) is not list else "".join([child.to_markdown() for child in self.text])
        match self.text_type:
            case "text":
                return selftext
            case "bold":
                return f"**{selftext}**"
            case "italic":
                return f"*{selftext}*"
            case "code":
                return f"`{selftext}`"
            case "link":
                return f"[{selftext}]({self.url})"
            case "image":
                return f"![{selftext}]({self.url})"
            case _:
                raise ValueError("Unhandled Text Type")