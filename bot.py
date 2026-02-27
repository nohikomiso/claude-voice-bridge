import os
import sys
import discord
from dotenv import load_dotenv
from clipboard import ClipboardCopier

# 環境変数の読み込み
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_TARGET_CHANNEL_ID = os.getenv("DISCORD_TARGET_CHANNEL_ID")

if not DISCORD_BOT_TOKEN or not DISCORD_TARGET_CHANNEL_ID:
    print("[エラー] .env ファイルに DISCORD_BOT_TOKEN と DISCORD_TARGET_CHANNEL_ID を設定してください。")
    sys.exit(1)

try:
    TARGET_CHANNEL_ID = int(DISCORD_TARGET_CHANNEL_ID)
except ValueError:
    print("[エラー] DISCORD_TARGET_CHANNEL_ID は数値である必要があります。")
    sys.exit(1)

# Discord クライアントの準備
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を読み取るために必要
client = discord.Client(intents=intents)

# コピー用クラスのインスタンス化
copier = ClipboardCopier()

@client.event
async def on_ready():
    print(f"[{client.user}] としてログインしました。")
    print(f"監視対象チャンネルID: {TARGET_CHANNEL_ID}")
    print("指定チャンネルにメッセージが送信されると、自動的にクリップボードにコピーされます。")
    print("終了するには Ctrl+C を押してください...\n")

@client.event
async def on_message(message):
    # Bot自身のメッセージは無視する
    if message.author == client.user:
        return

    # 指定されたチャンネル以外のメッセージは無視する
    if message.channel.id != TARGET_CHANNEL_ID:
        return

    # メッセージの内容があればクリップボードにコピーする
    if message.content:
        # 長い場合は省略して表示
        display_text = message.content[:50] + ('...' if len(message.content) > 50 else '')
        print(f"\n[受信] @{message.author}: {display_text}")
        try:
            copier.copy(message.content)
            print("-> クリップボードへのコピーに成功しました。")
        except Exception as e:
            print(f"-> [エラー] コピーに失敗しました: {e}")

if __name__ == "__main__":
    try:
        client.run(DISCORD_BOT_TOKEN)
    except Exception as e:
        print(f"[エラー] Botの起動に失敗しました: {e}")
