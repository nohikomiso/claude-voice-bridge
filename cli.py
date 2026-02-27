import argparse
import sys
from clipboard import ClipboardCopier

def main():
    parser = argparse.ArgumentParser(
        description="テキストをクリップボードにコピーするツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  uv run python cli.py "ここにテキストを入力"
"""
    )

    parser.add_argument(
        "text",
        help="クリップボードにコピーするテキスト内容"
    )

    args = parser.parse_args()

    try:
        copier = ClipboardCopier()
        copier.copy(args.text)

    except Exception as e:
        print(f"\n[エラー] 実行中にエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
