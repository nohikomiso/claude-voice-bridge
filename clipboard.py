import os
import shutil
import subprocess
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

        # Wayland環境の検出
        is_wayland = (
            "WAYLAND_DISPLAY" in os.environ
            or os.environ.get("XDG_SESSION_TYPE") == "wayland"
        )

        if is_wayland:
            wl_copy_path = shutil.which("wl-copy")
            if wl_copy_path:
                try:
                    subprocess.run([wl_copy_path], input=text, text=True, check=True)
                    print(
                        "コピー完了 (Wayland/wl-copy)。任意の場所に手動でペースト（Ctrl+V または Shift+Insert）してください。"
                    )
                    return True
                except subprocess.SubprocessError as e:
                    print(f"\n[エラー] wl-copyによるコピーに失敗しました: {e}")
                    return False
            else:
                print(
                    "\n[エラー] クリップボードへのアクセス機能が見つかりませんでした。"
                )
                print(
                    "Linux (Wayland環境) をご使用の場合は、以下のコマンドで wl-clipboard をインストールしてください:"
                )
                print("  sudo apt install wl-clipboard")
                return False

        # 非Wayland環境（X11, macOS, Windowsなど）の場合はpyperclipを使用
        try:
            pyperclip.copy(text)
            print(
                "コピー完了。任意の場所に手動でペースト（Ctrl+V または Shift+Insert）してください。"
            )
            return True
        except PyperclipException:
            print("\n[エラー] クリップボードへのアクセス機能が見つかりませんでした。")
            print(
                "Linux (Ubuntu等のX11環境) をご使用の場合は、以下のコマンドで xclip をインストールしてください:"
            )
            print("  sudo apt install xclip")
            return False
