# 実装計画

## Context

スマートフォンの音声入力を Discord 経由で PC に届け、クリップボードへコピーすることで、Claude Code 等の CLI ツールへの長文入力を楽にする。既存の有料音声入力ツールは Linux 非対応が多いため、OS 標準の音声入力 + Discord をインターフェースに採用した。

初期 PoC ではキーボードエミュレーションによる自動ペーストを検討したが、**クリップボードへのコピーのみ**に仕様を統一した。

## 現行アーキテクチャ

| ファイル | 役割 |
|---------|------|
| `clipboard.py` | `ClipboardCopier` — Wayland / pyperclip によるクリップボード操作 |
| `bot.py` | Discord チャンネル監視 |
| `cli.py` | CLI からの直接コピー |

## セットアップ・実行

```bash
uv sync
cp .env.example .env   # トークン・チャンネルIDを設定
uv run python bot.py   # Discord 監視モード
uv run python cli.py "テキスト"  # CLI コピーモード
```

## 検証手順

1. `.env` を設定し `uv run python bot.py` で Bot を起動する。
2. スマホの Discord から対象チャンネルにメッセージを送る。
3. PC 側でクリップボードにテキストが入っていることを確認し、エディタ等でペーストする。
