# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要
- プロジェクト: `claude-voice-bridge`
- 目的: Discordチャンネルを監視し、投稿されたメッセージをローカルのクリップボード（`pyperclip`）に自動でコピーするツール。ターミナル等のCLIツール（Claude Code等）にペーストする際の手間を削減します。
- 開発経緯: AquaVoice などの既存ツールが高価であること、および Ubuntu 非対応であることへの解決策として、Discord 経由のスマホ音声入力を採用。
- 旧仕様からの方針変更: キーボードエミュレーションによる自動ペーストは廃止し、「クリップボードへのコピーだけを行う」シンプルな仕様に統一しています。

## 開発環境・ツール
- **パッケージマネージャ**: `uv` を使用。
- **Pythonバージョン**: Python 3.13
- **依存関係**: `discord.py`, `python-dotenv`, `pyperclip`（Linux X11 では `xclip`、Wayland では `wl-clipboard` が別途必要）

## コマンド・運用ルール
当プロジェクトではシステムの破壊を防ぐため、**`python` や `pip` の直接実行、および仮想環境の手動アクティベート (`source .venv/Scripts/activate` 等) は禁止**されています。また `uv pip` などの互換コマンドも使用せず、必ず `uv` のネイティブコマンドを使用してください。
Claude Code 上では、これらを防ぐための Hook (`.claude/hooks/check_commands.py`) が導入されており、違反するコマンドは自動でブロックされます。

**許可・推奨されるコマンド**:
- スクリプトの実行 (Discord Bot): `uv run python bot.py`
- スクリプトの実行 (CUIで直接コピー): `uv run python cli.py "テキスト"`
- コードのチェック (Ruff): `uvx ruff check .`
- コードの自動整形 (Ruff): `uvx ruff format .`
- パッケージの追加: `uv add <package>`
- 依存関係の同期: `uv sync`

## 🛡️ コード品質チェックのルール (必須)
Pythonが実行時にコンパイルエラー（SyntaxError/NameError等）を起こすことを未然に防ぐため、**AI（Claude Code）がファイルの作成やコードの修正を行った後は、タスクを完了する前に必ず以下のコマンドを実行してコードの整合性を確認してください。**
```bash
uvx ruff check .
```
※警告やエラーが出た場合は、必ず自動修正 (`uvx ruff check --fix .`) または手動修正を行ってからユーザーに報告すること。

## アーキテクチャ構成
- `bot.py`: Discordサーバー上の特定チャンネルを監視し、新規メッセージを受信した際に `ClipboardCopier` を呼び出します。
- `cli.py`: コマンドラインから直接テキストを渡してクリップボードにコピーするためのエントリポイント。
- `clipboard.py`: コアロジックである `ClipboardCopier` クラスを提供。Wayland では `wl-copy`、それ以外では `pyperclip` 経由でOSのクリップボードへテキストをセットします。

## 機密情報の管理
- `.env` ファイルに `DISCORD_BOT_TOKEN` および `DISCORD_TARGET_CHANNEL_ID` を保存して運用します。
- `.env` は `.gitignore` によってGit管理から除外されているため、コミットしてはなりません。
