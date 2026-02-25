import unittest

from textnode import TextNode, TextType
from split_node_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    # ===== コードブロック (`code`) =====
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is text with a ", TextType.CODE),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.CODE),
            ],
        )

    # ===== ボールド (**bold**) =====
    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.BOLD),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.BOLD),
            ],
        )

    # ===== イタリック (_italic_) =====
    def test_italic_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.ITALIC),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.ITALIC),
            ],
        )

    # ===== デリミタが先頭にある場合 =====
    def test_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("", TextType.CODE),
                TextNode("code", TextType.CODE),
                TextNode(" at start", TextType.CODE),
            ],
        )

    # ===== デリミタが末尾にある場合 =====
    def test_delimiter_at_end(self):
        node = TextNode("ends with `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("ends with ", TextType.CODE),
                TextNode("code", TextType.CODE),
                TextNode("", TextType.CODE),
            ],
        )

    # ===== デリミタが含まれない場合 =====
    def test_no_delimiter(self):
        node = TextNode("plain text without delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [TextNode("plain text without delimiters", TextType.CODE)],
        )

    # ===== 複数のデリミタ出現 =====
    def test_multiple_delimiters(self):
        node = TextNode("a `first` b `second` c", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("a ", TextType.CODE),
                TextNode("first", TextType.CODE),
                TextNode(" b ", TextType.CODE),
                TextNode("second", TextType.CODE),
                TextNode(" c", TextType.CODE),
            ],
        )

    # ===== 非TEXTノードはそのまま通過する =====
    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    # ===== 複数ノードの混合入力 =====
    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("hello `world`", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("`code` here", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("hello ", TextType.CODE),
                TextNode("world", TextType.CODE),
                TextNode("", TextType.CODE),
                TextNode("bold text", TextType.BOLD),
                TextNode("", TextType.CODE),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.CODE),
            ],
        )

    # ===== 空リスト入力 =====
    def test_empty_list(self):
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])

    # ===== 空文字列ノード =====
    def test_empty_string_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("", TextType.CODE)])

    # ===== テキスト全体がデリミタ内 =====
    def test_entire_text_inside_delimiter(self):
        node = TextNode("`everything is code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("", TextType.CODE),
                TextNode("everything is code", TextType.CODE),
                TextNode("", TextType.CODE),
            ],
        )


if __name__ == "__main__":
    unittest.main()
