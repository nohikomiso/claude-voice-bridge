import pyperclip

class ClipboardCopier:
    """クリップボードへのテキストコピーを行うクラス"""

    def copy(self, text: str) -> None:
        """
        指定されたテキストをクリップボードにコピーする。
        """
        print("クリップボードにコピーしています...")
        pyperclip.copy(text)
        print("コピー完了。任意の場所に手動でペースト（Ctrl+V または Shift+Insert）してください。")

