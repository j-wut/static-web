import re

from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

SYMMETRICAL_DELIMITERS = {
        '**': 'bold',
        '*': 'italics',
        '`': 'code',
        }
ASYMMETRICAL_DELIMITERS = {"{":"}", "[":"]"}
ASYMMETRICAL_DELIMITERS.update({v:k for k,v in ASYMMETRICAL_DELIMITERS.items()})
ALL_DELIMITERS = {**SYMMETRICAL_DELIMITERS, **ASYMMETRICAL_DELIMITERS}

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Unhandled Text Type")

def weave(l1, l2):
    return [item for i in range(max(len(l1),len(l2))) for item in [*l1[i:i+1],*l2[i:i+1]]]

# single_single
# double_single_ = split double -> single, single_single
# double_single_single = split first double -> single,single_single,_single
# double_double = don't split, since we can see the matching double
# double_triple = split the triple, leftover single after
# double_single_double = split first double to match next single, then single matches the first of the split, leftover single ie: single,single_single,_single, single
def split_string_to_text_nodes(input_string):
    class DelimStackNode():
        def __init__(self, delim, head, tail):
            self.delim = delim
            self.head = head
            self.tail = tail

        def __eq__(self, other):
            return self.delim == other.delim

    delimiter_stack = []
    current_results = []
    current_result_head = len(input_string)
    current_result_tail = 0
    t = 0
    while t < len(input_string):
        for i in range(1, len(input_string)-t+1):
            if delimiter_stack and input_string[t:t+i] == delimiter_stack[-1].delim: # exact match with previous delimiter
                head_node = delimiter_stack.pop()
                tail_node = DelimStackNode(input_string[t:t+i],t,t+i)
                if current_results and head_node.head < current_result_head:
                    if current_result_head > head_node.tail:
                        current_results.insert(0,TextNode(input_string[head_node.tail:current_result_head], "text"))
                    if current_result_tail < tail_node.head:
                        current_results.append(TextNode(input_string[current_result_tail:tail_node.head], "text"))
                    current_results = [TextNode(current_results, SYMMETRICAL_DELIMITERS[head_node.delim])]
                    current_result_head = head_node.head
                    current_result_tail = tail_node.tail
                else:
                    current_results.append(TextNode(input_string[head_node.tail:tail_node.head], SYMMETRICAL_DELIMITERS[head_node.delim]))
                    current_result_head = min(current_result_head, head_node.head)
                    current_result_tail = max(current_result_tail, tail_node.tail)
                t += i
                break
            
            if input_string[t:t+i] in SYMMETRICAL_DELIMITERS:
                continue
            elif i==1:
                t += i
                break
            else:
                delim = input_string[t:t+i-1]
                tail_node = DelimStackNode(delim, t, t+i-1)
                if tail_node in delimiter_stack:
                    while not delimiter_stack[-1] == tail_node:
                        delimiter_stack.pop()
                    head_node = delimiter_stack.pop()
                    if current_results and head_node.head < current_result_head:
                        if current_result_head > head_node.tail:
                            current_results.insert(0,TextNode(input_string[head_node.tail:current_result_head], "text"))
                        if current_result_tail < tail_node.head:
                            current_results.append(TextNode(input_string[current_result_tail:tail_node.head], "text"))
                        current_results = [TextNode(current_results, SYMMETRICAL_DELIMITERS[head_node.delim])]
                        current_result_head = head_node.head
                        current_result_tail = tail_node.tail
                    else:
                        current_results.append(TextNode(input_string[head_node.tail,tail_node.head], SYMMETRICAL_DELIMITERS[head_node.delim]))
                        current_result_head = min(current_result_head, head_node.head)
                        current_result_tail = max(current_result_tail, tail_node.tail)
                delimiter_stack.append(DelimStackNode(delim, t, t+i-1))
                t += i - 1
                break
    if current_result_head > 0:
        current_results.insert(0,TextNode(input_string[0:current_result_head], "text"))
    if current_result_tail < len(input_string):
        current_results.append(TextNode(input_string[current_result_tail:len(input_string)], "text"))
    return current_results

def extract_markdown_images(input_string):
    image_markdown_regex = r"!\[(.*?)\]\((.*?)\)"
    image_markdown_non_capturing = r"!\[(?:.*?)\]\((?:.*?)\)"
    matches = re.findall(image_markdown_regex, input_string)
    image_split = re.split(image_markdown_non_capturing, input_string)
    return image_split, matches

def extract_markdown_links(input_string):
    link_markdown_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    link_markdown_non_capturing = r"(?<!!)\[(?:.*?)\]\((?:.*?)\)"
    matches = re.findall(link_markdown_regex, input_string)
    link_split = re.split(link_markdown_non_capturing, input_string)
    return link_split, matches

def split_string_images(input_string):
    split_by_images, images = extract_markdown_images(input_string)
    image_nodes = [TextNode(image[0], "image", image[1]) for image in images]
    if image_nodes:
        text_nodes = [split_string_to_text_nodes(text) for text in split_by_images]
        return [node for node in weave(text_nodes, image_nodes) if node]

    
def split_string_links(input_string):
    split_by_links, links = extract_markdown_links(input_string)
    link_nodes = [TextNode(link[0], "link", link[1]) for link in links]
    if link_nodes:
        text_nodes = [split_string_to_text_nodes(text) for text in split_by_links]
        return [node for node in weave(text_nodes, link_nodes) if node]

def process_list_text_node(process, nodes):
    results = []
    for node in nodes:
        if type(node) is list:
            results.append(process_list_text_node(process, node))
        else:
            processed = process(nodes.text)
            results.append(TextNode(processed, node.text_type, node.url) if type(processed) is list else node)
    return results

def convert_string_to_text_nodes(input_string):
    nested_text_nodes = split_string_to_text_nodes(input_string)
    with_links = process_list_text_node(split_string_links, nested_text_nodes)
    with_images = process_list_text_node(split_string_images, with_links)
    return with_images