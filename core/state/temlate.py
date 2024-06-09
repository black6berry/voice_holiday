from aiogram.fsm.state import State, StatesGroup

class ActionTemplate(StatesGroup):
    """Класс для сбора данных при добавлении шаблона"""
    action = State()
    get_holiday = State()
    get_template = State()
    confirm_template_text = State()