import os
import shutil
from gencontent import generate_page


def copy_directory_recursive(source_path, dest_path):
    if not os.path.exists(source_path):
        raise ValueError(f"Source path does not exist {source_path}")
    files = os.listdir(source_path)
    for file in files:
        source_file_path = os.path.join(source_path, file)
        dest_file_path = os.path.join(dest_path, file)
        print(f"Copying {source_file_path} to {dest_file_path}")
        if os.path.isfile(source_file_path):
            shutil.copy(source_file_path, dest_file_path)
        else:
            os.mkdir(dest_file_path)
            copy_directory_recursive(source_file_path, dest_file_path)


def generate_page_recursive(source_path, template_path, dest_path):
    files = os.listdir(source_path)
    for file in files:
        source_file_path = os.path.join(source_path, file)
        dest_file_path = os.path.join(dest_path, file)
        if os.path.isfile(source_file_path) and source_file_path.endswith(".md"):
            html_dest_path = dest_file_path.replace(".md", ".html")
            generate_page(source_file_path, template_path, html_dest_path)
        elif os.path.isdir(source_file_path):
            os.makedirs(dest_file_path, exist_ok=True)
            generate_page_recursive(source_file_path, template_path, dest_file_path)


def main():
    current_dir = os.getcwd()
    static_source = os.path.join(current_dir, "static")
    public_dest = os.path.join(current_dir, "public")
    print(f"Cleaning public directory: {public_dest}")
    if os.path.exists(public_dest):
        shutil.rmtree(public_dest)
    os.mkdir(public_dest)
    print(f"Copying from {static_source} to {public_dest}")
    copy_directory_recursive(static_source, public_dest)
    content_source = os.path.join(current_dir, "content")
    template_path = os.path.join(current_dir, "template.html")
    print(f"Generating pages from {content_source} to {public_dest}")
    generate_page_recursive(content_source, template_path, public_dest)


main()
