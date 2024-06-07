from aiogram.fsm.state import State, StatesGroup

class AddTemplate(StatesGroup):
    """Класс для сбора данных при добавлении шаблона"""
    get_holiday_id = State()
    get_template_text = State()
    confirm_template_text = State()