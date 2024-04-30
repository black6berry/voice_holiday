from aiogram.filters.callback_data import CallbackData

class MyCallback(CallbackData, prefix="btn_text"):
    btn_txt: str

class UserAction(CallbackData, prefix="user_action"):
    click: str
    
class MenuCallBack(CallbackData, prefix="menu"):
    level: int
    menu_name: str
    category: int | None = None
    page: int = 1
    product_id: int | None = None
