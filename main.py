from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import client, admin
from data_base.db import init_db
import asyncio, config


bot = Bot(token=config.BOT_TOKEN)

dp = Dispatcher(storage=MemoryStorage())


def register_routers(dp):
    dp.include_router(client.router)
    dp.include_router(admin.router)


async def on_startup(dp):
    print("Bot is starting...")
    await init_db()


async def main():
    register_routers(dp)
    await on_startup(dp)
    print('Polling started...')
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())