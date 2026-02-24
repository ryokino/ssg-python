import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
