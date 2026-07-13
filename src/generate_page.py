import os
from block_markdown import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ").strip()
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path, basepath):
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
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))
    with open(dest_path, "w") as file:
        file.write(template)
    print(f"Page generated successfully at {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename).replace(".md", ".html")

        if os.path.isfile(from_path) and filename.endswith(".md"):
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
