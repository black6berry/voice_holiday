from aiogram.filters.callback_data import CallbackData

class MyCallback(CallbackData, prefix="btn_text"):
    btn_txt: str
    level: int

class UserAction(CallbackData, prefix="user_action"):
    click: str
    
