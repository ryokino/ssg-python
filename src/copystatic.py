import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    """
    ソースディレクトリの全内容を宛先ディレクトリへ再帰的にコピーする。
    宛先ディレクトリが存在する場合、まず全内容を削除してクリーンな状態にする。

    Args:
        source_dir_path: コピー元のディレクトリパス
        dest_dir_path: コピー先のディレクトリパス
    """
    if not os.path.exists(source_dir_path):
        raise ValueError(f"Source directory does not exist: {source_dir_path}")

    # 宛先ディレクトリが存在する場合は削除してクリーンにする
    if os.path.exists(dest_dir_path):
        print(f"Cleaning destination directory: {dest_dir_path}")
        shutil.rmtree(dest_dir_path)

    # 宛先ディレクトリを作成
    os.mkdir(dest_dir_path)
    print(f"Created directory: {dest_dir_path}")

    # ソースディレクトリの中身を走査
    for item in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path):
            # ファイルの場合はコピー
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")
        else:
            # ディレクトリの場合は再帰的にコピー
            # ここではrmtreeは不要（親で既に削除済み）なので、直接mkdirとコピーを行う
            _copy_dir_contents(source_path, dest_path)


def _copy_dir_contents(source_dir_path, dest_dir_path):
    """
    内部用の再帰コピー関数。rmtreeは行わない。

    Args:
        source_dir_path: コピー元のディレクトリパス
        dest_dir_path: コピー先のディレクトリパス
    """
    os.mkdir(dest_dir_path)
    print(f"Created directory: {dest_dir_path}")

    for item in os.listdir(source_dir_path):
        source_path = os.path.join(source_dir_path, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")
        else:
            _copy_dir_contents(source_path, dest_path)
