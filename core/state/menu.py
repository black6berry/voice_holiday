from aiogram.fsm.state import State, StatesGroup

class MenuState(StatesGroup):
    main_menu = State()
    get_holiday = State()
    get_template = State()
    get_template_text = State()
    get_voice = State()
    confirm_voice = State()
    get_firstname = State()
    get_lastname = State()
    get_patronymic = State()
    get_sender = State()
