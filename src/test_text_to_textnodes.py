import unittest

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    # ===== 全マークダウン構文の混合 =====
    def test_all_syntax_combined(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    # ===== プレーンテキストのみ =====
    def test_plain_text(self):
        text = "Just a plain sentence with no formatting"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [TextNode("Just a plain sentence with no formatting", TextType.TEXT)],
        )

    # ===== ボールドのみ =====
    def test_bold_only(self):
        text = "**bold text**"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("bold text", TextType.BOLD)])

    # ===== イタリックのみ =====
    def test_italic_only(self):
        text = "_italic text_"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("italic text", TextType.ITALIC)])

    # ===== コードのみ =====
    def test_code_only(self):
        text = "`code block`"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("code block", TextType.CODE)])

    # ===== 画像のみ =====
    def test_image_only(self):
        text = "![alt](https://example.com/img.png)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")],
        )

    # ===== リンクのみ =====
    def test_link_only(self):
        text = "[click here](https://example.com)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [TextNode("click here", TextType.LINK, "https://example.com")],
        )

    # ===== ボールドとイタリックの組み合わせ =====
    def test_bold_and_italic(self):
        text = "This is **bold** and _italic_ text"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    # ===== 複数のボールド =====
    def test_multiple_bold(self):
        text = "**first** and **second** bold"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("first", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.BOLD),
                TextNode(" bold", TextType.TEXT),
            ],
        )

    # ===== 複数のリンク =====
    def test_multiple_links(self):
        text = "Visit [google](https://google.com) and [github](https://github.com)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("github", TextType.LINK, "https://github.com"),
            ],
        )

    # ===== 複数の画像 =====
    def test_multiple_images(self):
        text = "![a](https://a.com/1.png) and ![b](https://b.com/2.png)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.IMAGE, "https://a.com/1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "https://b.com/2.png"),
            ],
        )

    # ===== 空文字列 =====
    def test_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        self.assertEqual(result, [])

    # ===== コードとリンクの組み合わせ =====
    def test_code_and_link(self):
        text = "Run `npm install` then visit [docs](https://docs.com)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("npm install", TextType.CODE),
                TextNode(" then visit ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://docs.com"),
            ],
        )

    # ===== 画像とリンクの混合 =====
    def test_image_and_link(self):
        text = (
            "See ![photo](https://img.com/photo.jpg) or click [here](https://link.com)"
        )
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("See ", TextType.TEXT),
                TextNode("photo", TextType.IMAGE, "https://img.com/photo.jpg"),
                TextNode(" or click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://link.com"),
            ],
        )

    # ===== 先頭がフォーマット済みテキスト =====
    def test_starts_with_formatting(self):
        text = "**bold** starts the sentence"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" starts the sentence", TextType.TEXT),
            ],
        )

    # ===== 末尾がフォーマット済みテキスト =====
    def test_ends_with_formatting(self):
        text = "sentence ends with `code`"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("sentence ends with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )


if __name__ == "__main__":
    unittest.main()
