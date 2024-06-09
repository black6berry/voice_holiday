from aiogram.fsm.state import State, StatesGroup

class MenuState(StatesGroup):
    """
        Класс для хранения состояния
        1.Выбор меню - main_menu
        2.Выбор праздника - get_holiday
        3.Выбор шаблона поздравлений - get_template
        4.Просмотр и подтверждение шаблона - get_template_text
        5.Выбор голоса диктора - get_voice
        6.Прослушивание и подтверждение голоса диктора - confirm_voice
        7.получение имени пользователя - get_firstname
        8.получение фамилии пользователя - get_lastname
        9.получение отчества пользователя - get_patronymic
        10.получение данных отпарвителя - get_sender
    """
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
    confirm_result = State()
