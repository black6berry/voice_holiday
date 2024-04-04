import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from core.utils.commands import set_command
from core.handlers import basic, callback
from core.db.database import sql_start 

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


router = Router()

""" Отправка сообщения админу при запуске бота """
async def start_bot(bot: Bot):
  await set_command(bot)
  try:
    await bot.send_message(chat_id=ADMIN_ID, text="Бот запущен!")
  except Exception as e:
    print(f"Не удалось отпарвить сообщение администратору - {ADMIN_ID}\n{e}")

""" Отправка сообщения админу при остановке бота """
async def stop_bot(bot: Bot):
  try:
    await bot.send_message(chat_id=ADMIN_ID, text="Бот остановлен!")
  except Exception as e:
    print(f"Не удалось отпарвить сообщение администратору - {ADMIN_ID}\n{e}")

async def main() -> None:
  bot = Bot(token=BOT_TOKEN)
  storage = MemoryStorage()
  dp = Dispatcher(token=BOT_TOKEN, storage=storage)

  dp.startup.register(start_bot)
  dp.shutdown.register(stop_bot)

  dp.include_routers(basic.router, callback.router)

  sql_start()
  try:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=['message', 'callback_query'])
  finally:
    bot.session.close()   


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())