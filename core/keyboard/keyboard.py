from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.handlers.factories import MyCallback
from core.keyboard import text_kb



def main_menu_admin_ikb() -> InlineKeyboardMarkup:
    """ Главное меню админа """
    ikb= InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.show_groups, callback_data=MyCallback(btn_txt="Показать группы").pack())
        ],
        [
            InlineKeyboardButton(text=text_kb.show_birthday_txt, callback_data=MyCallback(btn_txt="Тексты поздравлений").pack())
        ],
    ])
    return ikb

def users_action_ikb() -> InlineKeyboardMarkup:
    """ Клавиатура для действий с пользователями """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.list_back, callback_data=MyCallback(btn_txt="<<").pack()),
            InlineKeyboardButton(text=text_kb.list_next, callback_data=MyCallback(btn_txt=">>").pack()),
        ],
        [
            InlineKeyboardButton(text=text_kb.add_user, callback_data=MyCallback(btn_txt="Добавить пользователя").pack()),
            InlineKeyboardButton(text=text_kb.del_user, callback_data=MyCallback(btn_txt="Удалить пользователя").pack()),
        ],
        [
            InlineKeyboardButton(text=text_kb.main_menu, callback_data=MyCallback(btn_txt="Главное меню").pack())
        ],
    ])
    return ikb

"""Разметка клавиатуры для действий с группами"""
groups_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=text_kb.list_back, callback_data=MyCallback(btn_txt="<<").pack()),
        InlineKeyboardButton(text=text_kb.list_next, callback_data=MyCallback(btn_txt=">>").pack()),
    ],
    [
        InlineKeyboardButton(text=text_kb.add_group, callback_data=MyCallback(btn_txt="Добавить группу").pack()),
        InlineKeyboardButton(text=text_kb.del_group, callback_data=MyCallback(btn_txt="Удалить группу").pack()),
    ],
    [
        InlineKeyboardButton(text=text_kb.main_menu, callback_data=MyCallback(btn_txt="Главное меню").pack()),
    ],
])

"""Одиночная кнопка назад"""
back_ikb = InlineKeyboardMarkup(inline_keyboard=[
    {
        InlineKeyboardButton(text=text_kb.menu_back, callback_data=MyCallback(btn_txt="Назад").pack()),
    },
])
