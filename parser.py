from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME
from data_base.db import get_all_user_keywords

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def setup_parser(bot):
    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        text = event.message.message
        if not text:
            return

        all_users = get_all_user_keywords()

        for user_id, keywords in all_users.items():
            for kw in keywords:
                if kw.lower() in text.lower():
                    try:
                        await bot.send_message(user_id, f"🔍 Знайдено по <b>{kw}</b>:\n\n{text}")
                    except Exception as e:
                        print(f"[!] Помилка надсилання {user_id}: {e}")
                    break

async def start_telethon(bot):
    await client.start()
    await setup_parser(bot)
    print("🔎 Telethon parser запущено...")
