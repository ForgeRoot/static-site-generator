import os

from src.markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from src.markdown_html import get_heading_level, markdown_to_html_node

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            if get_heading_level(block) == 1:
                title = block.removeprefix('#')
                return title.lstrip()
    raise Exception("There is no title found")

def read_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
    return content

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_text = read_file(from_path)
    html_template = read_file(template_path)
    html_div_node = markdown_to_html_node(md_text)
    html_content = html_div_node.to_html()
    title = extract_title(md_text)
    html_template = html_template.replace("{{ Title }}", title)
    html_template = html_template.replace("{{ Content }}", html_content)
    html_template = html_template.replace('src="/', f'src="{basepath}')
    html_template = html_template.replace('href="/', f'href="{basepath}')
    with open(dest_path, 'w') as file:
        file.write(html_template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Generating dir from {dir_path_content} to {dest_dir_path} using {template_path}")
    for path in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, path)
        if os.path.isfile(from_path) and path.endswith(".md"):
            html_path = path.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, html_path)
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            new_dir_path_content = os.path.join(dir_path_content, path)
            new_dest_dir_path = os.path.join(dest_dir_path, path)
            print(f"created dir: {new_dest_dir_path}")
            os.makedirs(new_dest_dir_path)
            generate_page_recursive(new_dir_path_content, template_path, new_dest_dir_path, basepath)
