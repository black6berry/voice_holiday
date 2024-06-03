from aiogram.filters.callback_data import CallbackData

class MyCallback(CallbackData, prefix="btn_text"):
    btn_txt: str
    id: int
    level: int

class HolidayCallback(CallbackData, prefix="holiday"):
    holiday: str
    id: int

class HolidayTemplateCallback(CallbackData, prefix="holiday_template"):
    template: str
    id: int

class UserAction(CallbackData, prefix="user_action"):
    click: str
