import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from core.utils.commands import set_command
from core.handlers import basic, callback
from core.handlers.admin import callback as admin_callback
# from core.db.db_sqllite import sql_start
from core.config.config import BOT_TOKEN, admins, ADMIN_ID_LIST

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



router = Router()

async def start_bot(bot: Bot):
    """Отправка сообщения админу при запуске бота"""
    await set_command(bot)
    try:
        for admin in ADMIN_ID_LIST:
            await bot.send_message(chat_id=admin, text="Бот запущен!")
    except Exception as e:
        print(f"Не удалось отпарвить сообщение администратору - {admin}\n{e}")

async def stop_bot(bot: Bot):
    """Отправка сообщения админу при остановке бота"""
    try:
        for admin in ADMIN_ID_LIST:
            await bot.send_message(chat_id=admin, text="Бот остановлен!")
    except Exception as e:
        print(f"Не удалось отпарвить сообщение администратору - {admin  }\n{e}")

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(token=BOT_TOKEN, storage=storage)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(basic.router, callback.router, admin_callback.router)

    # sql_start()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=['message', 'callback_query'])
    finally:
        bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())