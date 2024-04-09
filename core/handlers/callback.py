from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext


from core.db.functions import get_birthday_text, get_users, get_groups 
from core.keyboard.keyboard import group_action_ikb, main_menu_admin_ikb, users_action_ikb
from aiogram.types import FSInputFile
from core.keyboard.keyboard import MyCallback


router = Router()

# Ф-я отображения групп
@router.callback_query(MyCallback.filter(F.btn_txt == "Группы"))
async def show_groups( callback: CallbackQuery, bot: Bot ) -> None:
  
  groups = get_groups()

  if groups != None:
    msg_txt = "ID | Name\n"
    for group in groups:
      msg_txt += f"{group['ID']} - {group['Name']}\n"
  else:
    msg_txt = "Нет групп"

  await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=group_action_ikb())
  await callback.answer()
  await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


# Ф-я отображения теккстов поздравлений
@router.callback_query(MyCallback.filter(F.btn_txt == "Тексты поздравлений"))
async def show_birthday_text( callback: CallbackQuery, bot: Bot ) -> None:
  
  birthday_texts = get_birthday_text()

  if birthday_texts != None:
    msg_txt = "ID | Name\n"
    for text in birthday_texts:
      msg_txt += f"{text['ID']} - {text['Name']}\n"
  else:
    msg_txt = "Нет текстов поздравлений"

  await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=group_action_ikb())
  await callback.answer()
  await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


# Ф-я отображения пользователей
@router.callback_query(MyCallback.filter(F.btn_txt == "Показать пользователей"))
async def show_users( callback: CallbackQuery, bot: Bot ) -> None:

  users = get_users()
  
  if users != None:
    msg_txt = "ID | Name\n"
    for user in users:
      msg_txt += f"{user['ID']} - {user['Name']}\n"
  else:
    msg_txt = "Нет групп"

  await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=users_action_ikb())
  await callback.answer()
  await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


# Ф-я возврата в главное меню
@router.callback_query(MyCallback.filter(F.btn_txt == "Назад"))
async def show_main_menu( callback: CallbackQuery, bot: Bot ) -> None:
  
  msg_txt = "Главное меню"

  await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=main_menu_admin_ikb())
  await callback.answer()
  await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)