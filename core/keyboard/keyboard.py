from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.handlers.factories import MyCallback
from core.keyboard import text_kb



def main_menu_ikb() -> InlineKeyboardMarkup:
    """ Главное меню админа """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.choose_type_holiday, callback_data="выбрать праздник")
        ],
    ])
    return ikb


def choose_and_back_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.menu_back, callback_data="назад"),
            InlineKeyboardButton(text=text_kb.menu_choose, callback_data="выбрать")
        ],
    ])
    return ikb


def yes_and_back_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.menu_back, callback_data="назад"),
            InlineKeyboardButton(text=text_kb.menu_yes, callback_data="да")
        ],
    ])
    return ikb