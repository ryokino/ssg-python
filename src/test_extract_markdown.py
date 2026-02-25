import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This has an image ![alt text](https://example.com/img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/img.png")])

    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(
            result,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_no_images(self):
        text = "This is plain text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_image_with_empty_alt(self):
        text = "Image with no alt ![](https://example.com/img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "https://example.com/img.png")])

    def test_image_not_confused_with_link(self):
        text = "A link [click here](https://example.com) should not match"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_image_with_special_chars_in_alt(self):
        text = "![image (1) & 2](https://example.com/img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image (1) & 2", "https://example.com/img.png")])

    def test_image_mixed_with_text(self):
        text = "before ![img](https://example.com/a.png) middle ![img2](https://example.com/b.png) after"
        result = extract_markdown_images(text)
        self.assertEqual(
            result,
            [
                ("img", "https://example.com/a.png"),
                ("img2", "https://example.com/b.png"),
            ],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "This has a [link](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://example.com")])

    def test_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(
            result,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_no_links(self):
        text = "This is plain text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_link_with_empty_text(self):
        text = "Empty link [](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "https://example.com")])

    def test_link_with_special_chars_in_url(self):
        text = "Check [this](https://example.com/path?q=hello&lang=en)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("this", "https://example.com/path?q=hello&lang=en")])

    def test_link_at_start_of_text(self):
        text = "[first](https://first.com) and then more text"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("first", "https://first.com")])

    def test_link_at_end_of_text(self):
        text = "Click here [last](https://last.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("last", "https://last.com")])

    def test_multiple_links_adjacent(self):
        text = "[a](https://a.com)[b](https://b.com)"
        result = extract_markdown_links(text)
        self.assertEqual(
            result,
            [("a", "https://a.com"), ("b", "https://b.com")],
        )

    def test_empty_string(self):
        text = ""
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_link_with_anchor(self):
        text = "Go to [section](https://example.com/page#heading)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("section", "https://example.com/page#heading")])


if __name__ == "__main__":
    unittest.main()
