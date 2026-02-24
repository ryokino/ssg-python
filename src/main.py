from textnode import TextNode


def main():
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")  # noqa: F821
    print(text_node)


if __name__ == "__main__":
    main()
