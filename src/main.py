import os
import shutil

from copy_static import copy_files_recursive
from generate_page import generate_page, generate_page_recursive

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print("Copying static files to public directory...")
    copy_files_recursive("static", "public")
    generate_page_recursive("content", "template.html", "public")



if __name__ == "__main__":
    main()
