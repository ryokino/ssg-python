import unittest

from markdown_to_blocks import BlockType, block_to_block_type


class TestBlockToBlockTypeHeading(unittest.TestCase):
    """見出し (heading) のテスト"""

    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.heading)

    def test_heading_h2(self):
        self.assertEqual(block_to_block_type("## Hello"), BlockType.heading)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Hello"), BlockType.heading)

    def test_heading_h4(self):
        self.assertEqual(block_to_block_type("#### Hello"), BlockType.heading)

    def test_heading_h5(self):
        self.assertEqual(block_to_block_type("##### Hello"), BlockType.heading)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Hello"), BlockType.heading)

    def test_heading_h1_long_text(self):
        self.assertEqual(
            block_to_block_type("# This is a longer heading with multiple words"),
            BlockType.heading,
        )

    def test_heading_h2_with_special_chars(self):
        self.assertEqual(
            block_to_block_type("## Heading with **bold** and _italic_"),
            BlockType.heading,
        )

    def test_heading_7_hashes_is_paragraph(self):
        """7個の # はパラグラフになる"""
        self.assertEqual(
            block_to_block_type("####### Not a heading"), BlockType.paragraph
        )

    def test_heading_8_hashes_is_paragraph(self):
        """8個の # もパラグラフ"""
        self.assertEqual(
            block_to_block_type("######## Not a heading"), BlockType.paragraph
        )

    def test_heading_no_space_after_hash(self):
        """# の後にスペースがない場合はパラグラフ"""
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.paragraph)

    def test_heading_no_space_h2(self):
        """## の後にスペースがない場合はパラグラフ"""
        self.assertEqual(block_to_block_type("##NoSpace"), BlockType.paragraph)

    def test_heading_only_hash_and_space(self):
        """# + スペースのみ（テキストなし）でも見出し"""
        self.assertEqual(block_to_block_type("# "), BlockType.heading)

    def test_heading_single_char(self):
        self.assertEqual(block_to_block_type("# A"), BlockType.heading)


class TestBlockToBlockTypeCode(unittest.TestCase):
    """コードブロック (code) のテスト"""

    def test_code_block_basic(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"), BlockType.code
        )

    def test_code_block_with_language(self):
        self.assertEqual(
            block_to_block_type("```python\nprint('hello')\n```"), BlockType.code
        )

    def test_code_block_multiline(self):
        code = "```\nline1\nline2\nline3\n```"
        self.assertEqual(block_to_block_type(code), BlockType.code)

    def test_code_block_empty(self):
        """空のコードブロック"""
        self.assertEqual(block_to_block_type("```\n```"), BlockType.code)

    def test_code_block_minimal(self):
        """最小のコードブロック（開始と終了が連結）"""
        self.assertEqual(block_to_block_type("``````"), BlockType.code)

    def test_code_block_no_closing(self):
        """閉じ ``` がない場合はパラグラフ"""
        self.assertEqual(
            block_to_block_type("```\nprint('hello')"), BlockType.paragraph
        )

    def test_code_block_no_opening(self):
        """開き ``` がない場合はパラグラフ"""
        self.assertEqual(
            block_to_block_type("print('hello')\n```"), BlockType.paragraph
        )

    def test_code_block_with_backticks_inside(self):
        """コードブロック内にバッククォートを含む"""
        code = "```\nuse `inline code` here\n```"
        self.assertEqual(block_to_block_type(code), BlockType.code)

    def test_code_block_with_special_content(self):
        """特殊文字を含むコードブロック"""
        code = "```\n> not a quote\n- not a list\n# not a heading\n```"
        self.assertEqual(block_to_block_type(code), BlockType.code)


class TestBlockToBlockTypeQuote(unittest.TestCase):
    """引用ブロック (quote) のテスト"""

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.quote)

    def test_quote_single_line_with_space(self):
        self.assertEqual(block_to_block_type("> quote"), BlockType.quote)

    def test_quote_multiline(self):
        quote = "> line 1\n> line 2\n> line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.quote)

    def test_quote_multiline_no_space(self):
        """各行の > の後にスペースがなくてもOK"""
        quote = ">line 1\n>line 2\n>line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.quote)

    def test_quote_mixed_spaces(self):
        """スペースありなしが混在してもOK"""
        quote = "> line 1\n>line 2\n> line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.quote)

    def test_quote_not_all_lines_start_with_gt(self):
        """全行が > で始まらない場合はパラグラフ"""
        quote = "> line 1\nline 2\n> line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.paragraph)

    def test_quote_second_line_missing_gt(self):
        """2行目に > がない"""
        quote = "> first\nsecond"
        self.assertEqual(block_to_block_type(quote), BlockType.paragraph)

    def test_quote_nested(self):
        """ネストされた引用"""
        quote = "> outer\n>> inner\n> outer again"
        self.assertEqual(block_to_block_type(quote), BlockType.quote)

    def test_quote_with_empty_quote_line(self):
        """空の引用行（> のみ）"""
        quote = "> line 1\n>\n> line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.quote)


class TestBlockToBlockTypeUnorderedList(unittest.TestCase):
    """順序なしリスト (unordered_list) のテスト"""

    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.unordered_list)

    def test_unordered_list_multiple_items(self):
        ul = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.unordered_list)

    def test_unordered_list_many_items(self):
        ul = "- a\n- b\n- c\n- d\n- e"
        self.assertEqual(block_to_block_type(ul), BlockType.unordered_list)

    def test_unordered_list_with_special_content(self):
        """リスト項目に特殊文字"""
        ul = "- **bold** item\n- _italic_ item\n- `code` item"
        self.assertEqual(block_to_block_type(ul), BlockType.unordered_list)

    def test_unordered_list_missing_space(self):
        """- の後にスペースがない場合はパラグラフ"""
        self.assertEqual(block_to_block_type("-item"), BlockType.paragraph)

    def test_unordered_list_not_all_lines(self):
        """全行が - で始まらない場合はパラグラフ"""
        ul = "- item 1\nitem 2\n- item 3"
        self.assertEqual(block_to_block_type(ul), BlockType.paragraph)

    def test_unordered_list_second_line_missing_dash(self):
        """2行目に - がない"""
        ul = "- first\nsecond"
        self.assertEqual(block_to_block_type(ul), BlockType.paragraph)

    def test_unordered_list_second_line_missing_space(self):
        """2行目に - はあるがスペースがない"""
        ul = "- first\n-second"
        self.assertEqual(block_to_block_type(ul), BlockType.paragraph)

    def test_unordered_list_long_items(self):
        """長いテキストのリスト項目"""
        ul = "- This is a very long list item with multiple words\n- Another long item here"
        self.assertEqual(block_to_block_type(ul), BlockType.unordered_list)


class TestBlockToBlockTypeOrderedList(unittest.TestCase):
    """順序付きリスト (ordered_list) のテスト"""

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ordered_list)

    def test_ordered_list_two_items(self):
        ol = "1. first\n2. second"
        self.assertEqual(block_to_block_type(ol), BlockType.ordered_list)

    def test_ordered_list_three_items(self):
        ol = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ol), BlockType.ordered_list)

    def test_ordered_list_five_items(self):
        ol = "1. a\n2. b\n3. c\n4. d\n5. e"
        self.assertEqual(block_to_block_type(ol), BlockType.ordered_list)

    def test_ordered_list_ten_items(self):
        ol = "\n".join(f"{i + 1}. item {i + 1}" for i in range(10))
        self.assertEqual(block_to_block_type(ol), BlockType.ordered_list)

    def test_ordered_list_wrong_start_number(self):
        """2から始まる場合はパラグラフ"""
        ol = "2. first\n3. second"
        self.assertEqual(block_to_block_type(ol), BlockType.paragraph)

    def test_ordered_list_wrong_order(self):
        """番号が順番通りでない場合はパラグラフ"""
        ol = "1. first\n3. second\n2. third"
        self.assertEqual(block_to_block_type(ol), BlockType.paragraph)

    def test_ordered_list_duplicate_numbers(self):
        """同じ番号が重複する場合はパラグラフ"""
        ol = "1. first\n1. second\n1. third"
        self.assertEqual(block_to_block_type(ol), BlockType.paragraph)

    def test_ordered_list_missing_space(self):
        """番号の後にスペースがない場合はパラグラフ"""
        self.assertEqual(block_to_block_type("1.item"), BlockType.paragraph)

    def test_ordered_list_missing_dot(self):
        """ドットがない場合はパラグラフ"""
        self.assertEqual(block_to_block_type("1 item"), BlockType.paragraph)

    def test_ordered_list_with_special_content(self):
        """リスト項目に特殊文字"""
        ol = "1. **bold**\n2. _italic_\n3. `code`"
        self.assertEqual(block_to_block_type(ol), BlockType.ordered_list)

    def test_ordered_list_second_line_not_numbered(self):
        """2行目が番号付きでない"""
        ol = "1. first\nnot numbered"
        self.assertEqual(block_to_block_type(ol), BlockType.paragraph)

    def test_ordered_list_skipped_number(self):
        """番号が飛んでいる (1, 2, 4)"""
        ol = "1. first\n2. second\n4. fourth"
        self.assertEqual(block_to_block_type(ol), BlockType.paragraph)


class TestBlockToBlockTypeParagraph(unittest.TestCase):
    """パラグラフ (paragraph) のテスト"""

    def test_paragraph_simple(self):
        self.assertEqual(
            block_to_block_type("This is a paragraph"), BlockType.paragraph
        )

    def test_paragraph_multiline(self):
        p = "This is line 1\nThis is line 2"
        self.assertEqual(block_to_block_type(p), BlockType.paragraph)

    def test_paragraph_with_inline_code(self):
        self.assertEqual(
            block_to_block_type("This has `inline code` inside"), BlockType.paragraph
        )

    def test_paragraph_with_bold(self):
        self.assertEqual(
            block_to_block_type("This has **bold** text"), BlockType.paragraph
        )

    def test_paragraph_with_italic(self):
        self.assertEqual(
            block_to_block_type("This has _italic_ text"), BlockType.paragraph
        )

    def test_paragraph_starts_with_number_no_dot(self):
        """数字で始まるがリスト形式でない"""
        self.assertEqual(
            block_to_block_type("100 reasons to learn Python"), BlockType.paragraph
        )

    def test_paragraph_starts_with_dash_no_space(self):
        """- で始まるがスペースがない"""
        self.assertEqual(block_to_block_type("-not a list"), BlockType.paragraph)

    def test_paragraph_single_word(self):
        self.assertEqual(block_to_block_type("Hello"), BlockType.paragraph)

    def test_paragraph_empty_string(self):
        """空文字列はパラグラフ"""
        self.assertEqual(block_to_block_type(""), BlockType.paragraph)

    def test_paragraph_only_spaces(self):
        self.assertEqual(block_to_block_type("   "), BlockType.paragraph)

    def test_paragraph_that_looks_like_heading_no_space(self):
        """###テスト は見出しではなくパラグラフ"""
        self.assertEqual(block_to_block_type("###テスト"), BlockType.paragraph)

    def test_paragraph_hash_in_middle(self):
        """途中に # があるテキスト"""
        self.assertEqual(
            block_to_block_type("This is not a # heading"), BlockType.paragraph
        )

    def test_paragraph_gt_in_middle(self):
        """途中に > があるテキスト"""
        self.assertEqual(
            block_to_block_type("This is not > a quote"), BlockType.paragraph
        )


class TestBlockToBlockTypeEdgeCases(unittest.TestCase):
    """エッジケースのテスト"""

    def test_heading_with_trailing_hashes(self):
        """末尾に # がある見出し"""
        self.assertEqual(block_to_block_type("## Heading ##"), BlockType.heading)

    def test_quote_single_gt(self):
        """> のみの行"""
        self.assertEqual(block_to_block_type(">"), BlockType.quote)

    def test_unordered_list_item_with_nested_content(self):
        """リスト項目にネストコンテンツっぽいもの"""
        ul = "- item 1\n- item 2 with > quote\n- item 3 with # heading"
        self.assertEqual(block_to_block_type(ul), BlockType.unordered_list)

    def test_ordered_list_item_with_nested_content(self):
        """番号付きリスト項目にネストコンテンツっぽいもの"""
        ol = "1. item with > quote\n2. item with # heading\n3. item with - dash"
        self.assertEqual(block_to_block_type(ol), BlockType.ordered_list)

    def test_code_block_with_hash_content(self):
        """コードブロック内に # がある"""
        code = "```\n# this is a comment\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.code)

    def test_code_block_with_list_content(self):
        """コードブロック内にリストっぽい内容"""
        code = "```\n- not a list\n1. not ordered\n```"
        self.assertEqual(block_to_block_type(code), BlockType.code)

    def test_only_backticks_three(self):
        """バッククォート3つだけ → 開始と終了が同じなのでコード"""
        self.assertEqual(block_to_block_type("```"), BlockType.code)

    def test_heading_h1_with_multiple_spaces(self):
        """# の後にスペースが複数あっても見出し"""
        self.assertEqual(block_to_block_type("#  multiple spaces"), BlockType.heading)

    def test_gt_on_first_line_but_not_second(self):
        """> が最初の行にだけある"""
        self.assertEqual(block_to_block_type("> first\nsecond"), BlockType.paragraph)

    def test_dash_on_first_line_but_not_second(self):
        """- が最初の行にだけある"""
        self.assertEqual(block_to_block_type("- first\nsecond"), BlockType.paragraph)


if __name__ == "__main__":
    unittest.main()
