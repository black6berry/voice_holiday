from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.handlers.factories import MyCallback
from core.keyboard import text_kb



def main_menu_ikb() -> InlineKeyboardMarkup:
    """ Главное меню админа """
    ikb= InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.choose_type_holiday, callback_data=MyCallback(btn_txt="выбрать праздник", level=0).pack())
        ],
    ])
    return ikb


def holidays_ikb() -> InlineKeyboardMarkup:
    """ Выбор праздика """
    ikb= InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_kb.holiday_birthday, callback_data=MyCallback(btn_txt="день рождения", level=1).pack()),
            InlineKeyboardButton(text=text_kb.holiday_defenderday, callback_data=MyCallback(btn_txt="день защитника отечества", level=1).pack())
        ],
        [
            InlineKeyboardButton(text=text_kb.holiday_womensday, callback_data=MyCallback(btn_txt="женский день", level=1).pack()),
            InlineKeyboardButton(text=text_kb.holiday_allworkday, callback_data=MyCallback(btn_txt="день весны и труда", level=1).pack())
        ],
        [
            InlineKeyboardButton(text=text_kb.holiday_winnerday, callback_data=MyCallback(btn_txt="день победы", level=1).pack()),
            InlineKeyboardButton(text=text_kb.holiday_russiaday, callback_data=MyCallback(btn_txt="день России", level=1).pack())
        ],
        [
            InlineKeyboardButton(text=text_kb.holiday_nameday, callback_data=MyCallback(btn_txt="именины", level=1).pack()),
            InlineKeyboardButton(text=text_kb.holiday_unityday, callback_data=MyCallback(btn_txt="день народного единства", level=1).pack())
        ],
        [
            InlineKeyboardButton(text=text_kb.holiday_knowledgeday, callback_data=MyCallback(btn_txt="день знаний", level=1).pack()),
            InlineKeyboardButton(text=text_kb.holiday_14thday, callback_data=MyCallback(btn_txt="день влюбленных", level=1).pack())
        ],
        [
            InlineKeyboardButton(text=text_kb.create_holiday_yourself, callback_data=MyCallback(btn_txt="свой шаблон", level=1).pack())
        ]
    ])
    return ikb


"""Одиночная кнопка назад"""
back_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=text_kb.menu_back, callback_data=MyCallback(btn_txt="Назад", level=1).pack()),
    ],
])
