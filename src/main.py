from copystatic import copy_files_recursive
from generate_page import generate_page


def main():
    copy_files_recursive("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
