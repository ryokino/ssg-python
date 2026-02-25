import os
from markdown_to_html import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # マークダウンファイルを読み込む
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # テンプレートファイルを読み込む
    with open(template_path, "r") as f:
        template_content = f.read()

    # マークダウンをHTML文字列に変換
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # タイトルを取得
    title = extract_title(markdown_content)

    # テンプレートのプレースホルダーを置き換え
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # 必要なディレクトリを作成
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # HTMLファイルを書き込む
    with open(dest_path, "w") as f:
        f.write(full_html)
