from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext


from core.db.functions import get_users, get_groups 
from core.keyboard.keyboard import group_action_ikb, main_menu_admin_ikb, users_action_ikb
from aiogram.types import FSInputFile
from core.keyboard.keyboard import MyCallback


router = Router()

# Ф-я отображения пользователей
@router.callback_query(MyCallback.filter(F.btn_txt == "Показать пользователей"))
async def show_users( callback: CallbackQuery, bot: Bot ) -> None:

  msg_txt = get_users()

  # msg_txt = "Управление пользователями"

  await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=users_action_ikb())
  await callback.answer()
  await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

# Ф-я отображения групп
@router.callback_query(MyCallback.filter(F.btn_txt == "Показать группы"))
async def show_groups( callback: CallbackQuery, bot: Bot ) -> None:
  
  groups = get_groups()
  print(groups)

  msg_txt = "ID | Name\n"
  for group in groups:
    msg_txt += f"{group['ID']} - {group['Name']}\n"

  await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=group_action_ikb())
  await callback.answer()
  await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

# Ф-я возврата в главное меню
@router.callback_query(MyCallback.filter(F.btn_txt == "Назад"))
async def show_main_menu( callback: CallbackQuery, bot: Bot ) -> None:
  
  msg_txt = "Главное меню"

  await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=main_menu_admin_ikb())
  await callback.answer()
  await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)