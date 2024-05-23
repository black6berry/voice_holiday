from mailbox import Message
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import Bot, Router, F, types
from aiogram.fsm.context import FSMContext
from core.handlers.basic import get_start
from core.keyboard.keyboard import  main_menu_ikb, holidays_ikb
from core.keyboard.keyboard import MyCallback, back_ikb
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from core.state.menu import MenuState
from core.db.functions import ActionORM
from aiogram.filters import StateFilter
from core.keyboard import text_kb
from aiogram.filters.callback_data import CallbackData



router = Router()


@router.callback_query(StateFilter(MenuState.main_menu), MyCallback.filter(F.btn_txt.lower() == "выбрать праздник"))
async def show_type_holiays(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я отображения праздников"""
    await state.set_state(MenuState.menu_step2)
    msg_txt = "Выбери праздник или напиши свой текст поздравления"

    holidays = ActionORM.get_holidays()
    print(holidays)
    builder = InlineKeyboardBuilder()
    for holiday in holidays:
        builder.button(text=holiday['name'], callback_data=holiday['name'])
    builder.adjust(2)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text=text_kb.create_holiday_yourself, callback_data=MyCallback(btn_txt="cвой шаблон", level=1))
    builder.attach(another_builder)

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=builder.as_markup())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)




@router.callback_query(MyCallback.filter(F.btn_txt.lower().in_({"главное меню", "назад"})), StateFilter(MenuState.menu_step2))
async def go_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Обработка нажатия кнопки назад из состояния 'Показать поздравления'"""
    await state.set_state(MenuState.main_menu)
    msg_txt = " Voice Holiday - Сервис для поздравлений пользователей по системе радиовещания :D "
    await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=main_menu_ikb())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
