import os
from block_markdown import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ").strip()
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    title = extract_title(markdown)
    with open(template_path, "r") as file:
        template = file.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))
    with open(dest_path, "w") as file:
        file.write(template)
    print(f"Page generated successfully at {dest_path}")
