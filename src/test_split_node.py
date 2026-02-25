import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_images, split_nodes_links


# =====================================================================
# split_nodes_delimiter のテスト
# =====================================================================
class TestSplitNodesDelimiter(unittest.TestCase):
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

    def test_no_delimiter(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("plain text", TextType.CODE)])

    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_empty_list(self):
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])


# =====================================================================
# split_nodes_images のテスト
# =====================================================================
class TestSplitNodesImages(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "Text with ![alt](https://example.com/img.png) here",
            TextType.TEXT,
        )
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(result, [TextNode("Just plain text", TextType.TEXT)])

    def test_image_at_start(self):
        node = TextNode("![img](https://example.com/a.png) after", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [
                TextNode("img", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_image_at_end(self):
        node = TextNode("before ![img](https://example.com/a.png)", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [
                TextNode("before ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/a.png"),
            ],
        )

    def test_image_only(self):
        node = TextNode("![solo](https://example.com/solo.png)", TextType.TEXT)
        result = split_nodes_images([node])
        self.assertEqual(
            result,
            [TextNode("solo", TextType.IMAGE, "https://example.com/solo.png")],
        )

    def test_non_text_node_passes_through(self):
        node = TextNode("bold text", TextType.BOLD)
        result = split_nodes_images([node])
        self.assertEqual(result, [TextNode("bold text", TextType.BOLD)])

    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("before ![img](https://example.com/a.png) after", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("![img2](https://example.com/b.png)", TextType.TEXT),
        ]
        result = split_nodes_images(nodes)
        self.assertEqual(
            result,
            [
                TextNode("before ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" after", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("img2", TextType.IMAGE, "https://example.com/b.png"),
            ],
        )

    def test_empty_list(self):
        result = split_nodes_images([])
        self.assertEqual(result, [])


# =====================================================================
# split_nodes_links のテスト
# =====================================================================
class TestSplitNodesLinks(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "Click [here](https://example.com) now",
            TextType.TEXT,
        )
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_multiple_links(self):
        node = TextNode(
            "Visit [boot dev](https://www.boot.dev) and [youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(result, [TextNode("Just plain text", TextType.TEXT)])

    def test_link_at_start(self):
        node = TextNode("[first](https://first.com) then more", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("first", TextType.LINK, "https://first.com"),
                TextNode(" then more", TextType.TEXT),
            ],
        )

    def test_link_at_end(self):
        node = TextNode("click [last](https://last.com)", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("click ", TextType.TEXT),
                TextNode("last", TextType.LINK, "https://last.com"),
            ],
        )

    def test_link_only(self):
        node = TextNode("[solo](https://solo.com)", TextType.TEXT)
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [TextNode("solo", TextType.LINK, "https://solo.com")],
        )

    def test_non_text_node_passes_through(self):
        node = TextNode("italic text", TextType.ITALIC)
        result = split_nodes_links([node])
        self.assertEqual(result, [TextNode("italic text", TextType.ITALIC)])

    def test_multiple_nodes_mixed(self):
        nodes = [
            TextNode("go to [site](https://site.com) ok", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode("[another](https://another.com)", TextType.TEXT),
        ]
        result = split_nodes_links(nodes)
        self.assertEqual(
            result,
            [
                TextNode("go to ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://site.com"),
                TextNode(" ok", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode("another", TextType.LINK, "https://another.com"),
            ],
        )

    def test_link_with_query_params(self):
        node = TextNode(
            "Search [google](https://google.com/search?q=hello&lang=en) now",
            TextType.TEXT,
        )
        result = split_nodes_links([node])
        self.assertEqual(
            result,
            [
                TextNode("Search ", TextType.TEXT),
                TextNode(
                    "google", TextType.LINK, "https://google.com/search?q=hello&lang=en"
                ),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_empty_list(self):
        result = split_nodes_links([])
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
