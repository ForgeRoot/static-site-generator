import os
import shutil
import sys

from src.copy_static import copy_files_recursive
from src.generate_page import generate_page, generate_page_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_docs = "./docs"


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]  # First argument after script name
    else:
        basepath = "/"  # Default
    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)
    
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)
    generate_page_recursive("content", "template.html", dir_path_docs, basepath)



if __name__ == "__main__":
    main()
