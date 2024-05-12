from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.handlers.factories import MyCallback
from core.keyboard import text_kb



def main_menu_admin_ikb() -> InlineKeyboardMarkup:
    """ Главное меню админа """
    ikb= InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.show_users, callback_data=MyCallback(btn_txt="Показать пользователей").pack())
        ],
        [
            InlineKeyboardButton(text=text_kb.show_template_congratulaton, callback_data=MyCallback(btn_txt="Тексты поздравлений").pack())
        ],
    ])
    return ikb

def users_action_ikb() -> InlineKeyboardMarkup:
    """ Клавиатура для действий с пользователями """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.add_user, callback_data=MyCallback(btn_txt="Добавить пользователя").pack()),
            InlineKeyboardButton(text=text_kb.del_user, callback_data=MyCallback(btn_txt="Удалить пользователя").pack()),
        ],
        [
            InlineKeyboardButton(text=text_kb.main_menu, callback_data=MyCallback(btn_txt="Главное меню").pack())
        ],
    ])
    return ikb


def congratulations_action_ikb() -> InlineKeyboardMarkup:
    """ Клавиатура для действий с пользователями """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.add_template_congratulaton, callback_data=MyCallback(btn_txt="Добавить шаблон").pack()),
            InlineKeyboardButton(text=text_kb.del_template_congratulaton, callback_data=MyCallback(btn_txt="Удалить шаблон").pack()),
        ],
        [
            InlineKeyboardButton(text=text_kb.main_menu, callback_data=MyCallback(btn_txt="Главное меню").pack())
        ],
    ])
    return ikb


"""Одиночная кнопка назад"""
back_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=text_kb.menu_back, callback_data=MyCallback(btn_txt="Назад").pack()),
    ],
])
