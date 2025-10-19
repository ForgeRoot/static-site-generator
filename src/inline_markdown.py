from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        cursor = 0
        while text.find(delimiter, cursor) != -1:
            opening = text.find(delimiter, cursor)
            if opening == -1: 
                break
            if opening > cursor:
                new_nodes.append(TextNode(text[cursor:opening], TextType.TEXT))
            closing = text.find(delimiter, opening + len(delimiter))
            if closing == -1:
                raise Exception(f"missing closing delimiter: {delimiter}")
            new_nodes.append(TextNode(text[opening + len(delimiter): closing], text_type))
            cursor = closing + len(delimiter)

        if cursor < len(node.text):
            new_nodes.append(TextNode(text[cursor:], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
