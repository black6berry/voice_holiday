from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, \
  InlineKeyboardButton, KeyboardButton
from core.handlers.factories import MyCallback
from core.keyboard import text_kb



# Главное меню админа
def main_menu_admin_ikb() -> InlineKeyboardMarkup:
  ikb= InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(text=text_kb.show_users, callback_data=MyCallback(btn_txt="Показать пользователей").pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.show_groups, callback_data=MyCallback(btn_txt="Показать группы").pack())
    ],
  ])
  return ikb

# Клавиатура для действий с пользователями 
def users_action_ikb() -> InlineKeyboardMarkup:
  ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(text=text_kb.add_user, callback_data=MyCallback(btn_txt="Добавить пользователя").pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.del_user, callback_data=MyCallback(btn_txt="Удалить пользователя").pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.back, callback_data=MyCallback(btn_txt="Назад").pack())
    ],
  ])
  return ikb

# Клавиатур для действий с группами 
def group_action_ikb() -> InlineKeyboardMarkup:
  ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(text=text_kb.add_group, callback_data=MyCallback(btn_txt="Добавить группу").pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.del_group, callback_data=MyCallback(btn_txt="Удалить группу").pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.back, callback_data=MyCallback(btn_txt="Назад").pack())
    ],
  ])
  return ikb

# Клавиутура отправки контакта пользователя
def get_contact_user_kb() -> ReplyKeyboardMarkup:
  kb = ReplyKeyboardMarkup(keyboard=[
    [
      KeyboardButton(text=text_kb.contact, request_contact=True)
    ],
  ], resize_keyboard=True, one_time_keyboard=True)
  return kb