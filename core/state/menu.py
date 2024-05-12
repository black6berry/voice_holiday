from aiogram.fsm.state import State, StatesGroup

class MenuState(StatesGroup):
    main_menu = State()
    menu_step2 = State()
    menu_step3 = State()