# アーキテクチャ設計 (Design)

## 概要

`claude-voice-bridge` は、Discord などの外部ソースから受け取ったテキストを、ローカルPCのクリップボードにコピーするツールです。キーボードエミュレーションによる自動ペーストは行わず、ユーザーが任意のアプリで手動ペースト（`Ctrl+V` 等）する前提です。

## コア・コンポーネント

1. **`ClipboardCopier` クラス (`clipboard.py`)**
   - **責務**: OS・セッション種別の差異を吸収し、クリップボードへのテキストコピーを一元管理する。
   - **Wayland**: `wl-copy`（`wl-clipboard` パッケージ）を `subprocess` 経由で呼び出す。
   - **その他 (X11 / Windows / macOS)**: `pyperclip` を使用。Linux X11 では `xclip` が必要。

2. **Discord Bot (`bot.py`)**
   - **責務**: 指定チャンネルの新規メッセージを監視し、本文を `ClipboardCopier` に渡す。
   - **設定**: `.env` の `DISCORD_BOT_TOKEN`, `DISCORD_TARGET_CHANNEL_ID`。

3. **CLI エントリポイント (`cli.py`)**
   - **責務**: コマンドライン引数で受け取ったテキストを `ClipboardCopier` 経由でコピーする（テスト・補助用）。

## 将来の拡張設計

- **ローカルHTTP受信**: Discord の代わりに LAN 内の簡易 HTTP サーバーでテキストを受け取るアダプタ。
- **PRIMARY セレクション**: Linux のマウス中クリック用クリップボードへの対応。
- **クリップボード復元**: コピー前の内容を保存し、処理後に元に戻すオプション。
