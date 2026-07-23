<div align="center">
  <h1>claude-voice-bridge</h1>
  <p><strong>スマホの音声入力をPCのプロンプト直結させる「モバイル音声ブリッジ」ツール</strong></p>

  <p>
    <img src="https://img.shields.io/badge/python-3.13-blue.svg" alt="Python 3.13">
    <img src="https://img.shields.io/badge/framework-discord.py-5865F2.svg" alt="discord.py">
    <img src="https://img.shields.io/badge/package-uv-purple.svg" alt="uv">
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  </p>
</div>

---

## 📝 概要

Discord経由で受け取ったテキストを、PCのローカルクリップボードに自動転送するシンプルな連携ツールです。
特に、**スマートフォンの標準機能（iPhone/Androidのキーボード音声入力）** で話した内容をDiscord経由でPCへ飛ばし、PC側でペーストするだけのシームレスな体験を提供します。

### 👀 利用イメージ（どんな風に便利なの？）

専用ツールや複雑な設定は不要です。スマホの Discord に向かって話すだけで、PC のあらゆるエディタに長文を送り込めます。

```mermaid
flowchart LR
    phone["📱 音声入力"]
    discord["Discord"]
    bot["voice-bridge"]
    clip["クリップボード"]
    paste["Ctrl+V"]

    phone --> discord --> bot --> clip --> paste
```

#### 1. スマホから送信（Discord アプリ）

`#プライベートチャンネル` に音声入力でメッセージを送ります。

> 🎤 ReactとTailwindCSSを使って、ダークモード対応のログイン画面を作るコンポーネントのコードを書いて。

#### 2. PC でペースト（Claude Code / Cursor / VSCode 等）

Bot が受信と同時にクリップボードへコピーします。あとはお使いの環境でペーストするだけです。

> ❯ ReactとTailwindCSSを使って、ダークモード対応の...

| 環境 | ペースト操作 |
|------|-------------|
| 一般的なアプリ / エディタ | `Ctrl+V` / `Cmd+V` |
| Windows Terminal 等 | `Ctrl+Shift+V` または右クリック |
| 昔ながらのコンソール | `Shift+Insert` |

長文プロンプトをPCのキーボードでカチカチ打ち込む必要はもうありません。歩きながらでも、寝転がりながらでも、スマホの優秀な音声入力でアイデアを吹き込み、PCで即座に実行できます。

---

## 🎙️ なぜこのツールを作ったのか

PCに向かって長文のプロンプトを打ち込む際、「スマホの優れた音声入力がそのままPCで使えればいいのに」と感じたことはありませんか？

**📖 誕生秘話**
「Claude Code を音声でサクサク操作したい！」と思ったのが開発のきっかけです。
しかし、既存の有名な音声入力ツール（AquaVoice等）は月額費用が高価であり、何より **UbuntuなどのLinux環境に対応していない** という大きな問題がありました。

そこで、「誰もが持っているスマートフォンの超優秀なOS標準音声入力（iPhone/SiriやAndroid/Google）を使えば、OS問わず無料で最高の音声UXが構築できるのでは？」と考え、スマホから一番手軽にテキストを送れる Discord をインターフェースとして活用し、PC側でテキストを受け取ってクリップボードに入れるこの仕組みをDIYで開発しました。

---

## 🛠️ アーキテクチャと拡張性

現在はセットアップの手軽さからバックエンドに「Discord」を利用していますが、このツールの本質は **「外部からのテキストをPCのクリップボードに直送する」** ことにあります。

もしプライバシーの観点で「自分の声（テキスト）をDiscordの外部サーバー経由で送るのには抵抗がある」という場合でも、システムは小さく分離されています。
クリップボード転送のコアロジック（`clipboard.py`）を再利用し、Discord Botの代わりに **ローカルネットワークで完結する簡易HTTPサーバーやWebhook通信** などに改造することも容易です。DIYのベースとして様々な応用に活用してください。

---

## 🚀 セットアップ

### 1. 必要要件
- Python 3.13以上
- uv (高速なPythonパッケージマネージャ)
- クリップボード連携用のシステム依存（OSごと）:
  - **Windows / macOS**: 追加インストール不要（`pyperclip` がOS標準のクリップボードを利用）
  - **Linux (X11)**: `xclip`（`sudo apt install xclip`）
  - **Linux (Wayland)**: `wl-clipboard`（`sudo apt install wl-clipboard`）

### 2. インストール
```bash
# プロジェクトのクローンと移動
git clone https://github.com/nohikomiso/claude-voice-bridge.git
cd claude-voice-bridge

# 依存関係のインストール（仮想環境の自動構築）
uv sync
```

### 3. 環境設定
`.env.example` をコピーして設定ファイル `.env` を作成します。
```bash
cp .env.example .env
```

作成した `.env` ファイルに、後述の「Botの作成手順」で取得する情報を記載してください。
```env
DISCORD_BOT_TOKEN=あなたのBotトークン
DISCORD_TARGET_CHANNEL_ID=監視するチャンネルのID
```

---

## 🤖 Discord Bot の作成と導入 (初回必須)

このツールはDiscordの「Bot」として動作するため、あなた専用のBotを作り、自分のDiscordサーバー（チャンネル）に招待しておく必要があります。

**1. Botの作成とトークン(`DISCORD_BOT_TOKEN`)の取得**
- Discord Developer Portal にアクセスし、右上の「New Application」からアプリ名（何でもOK）をつけて作成します。
- 左メニューから **「Bot」** を選び、「Reset Token」ボタンを押して表示された長い英数字が **Botのトークン** です。これを `.env` に貼り付けます。（※パスワードと同じなので誰にも教えないでください）

**2. メッセージ読み取り権限の有効化 (⚠️絶対に忘れないでください)**
- 同じ「Bot」画面を下にスクロールすると **「Privileged Gateway Intents」** という項目があります。
- その中の **`MESSAGE CONTENT INTENT`** のスイッチを **オン（青色）** にして「Save Changes」を押します。（これがないとBotは文字を読み取れません）

**3. サーバーへの招待**
- 左メニュー **「OAuth2」** > **「URL Generator」** を開きます。
- `SCOPES` 欄で **`bot`** にチェックを入れます。
- 下に現れる `BOT PERMISSIONS` 欄で **`Read Message History`** と **`View Channels`** にチェックを入れます。
- 一番下に生成された **URL** をブラウザの新しいタブに貼り付けて開き、自分のサーバーを選択してBotを参加（招待）させます。

**4. チャンネルID(`DISCORD_TARGET_CHANNEL_ID`)の取得**
- Discordアプリまたはブラウザを開きます。
- 左下の歯車（ユーザー設定）> 「詳細設定」> **「開発者モード」** をオンにします。
- 監視したいチャンネル（例: 自分しかいないプライベートチャンネル）を右クリックし、一番下の **「チャンネルIDをコピー」** をクリックします。
- コピーした数字を `.env` に貼り付けます。

これで準備完了です！

---

## 💻 使い方

### Discord 監視モード（メイン）
Botを起動して、Discordからのメッセージ受信を待機します。

```bash
uv run python bot.py
```
> **💡 ヒント:** 起動後、スマホのDiscordから音声入力を使って対象チャンネルにメッセージを送信すると、即座に手元のPCのクリップボードにコピーされます。あとはエディタ等でお使いの環境に合わせたペースト（`Ctrl+V` 等）をするだけです。

### CLI コピーモード（テスト・補助用）
コマンドラインから直接テキストを渡してクリップボードにコピーします。

```bash
uv run python cli.py "コピーしたいテキスト"
```

---

## 🖥️ 対応環境（クリップボード）

| OS | 方式 | 必要なもの |
|----|------|-----------|
| Windows / macOS | `pyperclip` | 追加インストール不要 |
| Linux (X11) | `pyperclip` + `xclip` | `sudo apt install xclip` |
| Linux (Wayland) | `wl-copy` | `sudo apt install wl-clipboard` |

Wayland セッションでは `WAYLAND_DISPLAY` または `XDG_SESSION_TYPE=wayland` を検出し、自動的に `wl-copy` を使います。X11 や Windows/macOS では `pyperclip` を使います。

---

## 🗺️ 今後の展望
- **クリップボード連携の強化**: 現状は一般的な `CLIPBOARD` セレクション（`Ctrl+V` 用）のみの対応ですが、要望に応じてLinuxでの `PRIMARY` セレクション（マウス中クリック用）のサポート拡張などを検討しています。
- **ローカルHTTP受信**: Discord の代わりに、LAN内で完結する簡易HTTPサーバーからテキストを受け取る方式の追加。

---

## 🤖 AI によって生成されたコードです
本プロジェクトのコードおよびこのドキュメントは、すべて私と Claude Code（AnthropicのAI）のペアプログラミングによって作成されました。
もし変な挙動や見落とし、AI特有の奇妙なコード構成があっても、どうか優しい目で見守り、改善のPRをいただけると嬉しいです！

---

## 📄 ライセンス
このプロジェクトは MIT ライセンスの下で公開されています。詳細は LICENSE ファイルをご確認ください。