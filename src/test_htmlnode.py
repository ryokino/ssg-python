import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="hello")
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises(self):
        node = HTMLNode(tag="p", value="hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_all_args(self):
        child = HTMLNode(tag="span", value="child")
        node = HTMLNode(
            tag="div", value="parent", children=[child], props={"class": "container"}
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(div, parent, [HTMLNode(span, child, None, None)], {'class': 'container'})",
        )


if __name__ == "__main__":
    unittest.main()
