import pyperclip
from pyperclip import PyperclipException

class ClipboardCopier:
    """クリップボードへのテキストコピーを行うクラス"""

    def copy(self, text: str) -> bool:
        """
        指定されたテキストをクリップボードにコピーする。

        Returns:
            bool: コピーに成功した場合は True、失敗した場合は False を返す。
        """
        print("クリップボードにコピーしています...")
        try:
            pyperclip.copy(text)
            print("コピー完了。任意の場所に手動でペースト（Ctrl+V または Shift+Insert）してください。")
            return True
        except PyperclipException:
            print("\n[エラー] クリップボードへのアクセス機能が見つかりませんでした。")
            print("Linux (Ubuntu等のX11環境) をご使用の場合は、以下のコマンドで xclip をインストールしてください:")
            print("  sudo apt install xclip")
            print("※注意: 当ツールはWayland環境をサポートしていません。必要に応じてX11セッションをご利用ください。")
            return False

