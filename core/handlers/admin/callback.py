from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.db.functions import ActionORM
from core.filters.is_admin import IsAdmin
from textwrap import dedent
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.filters import StateFilter
from core.handlers.factories import HolidayCallback
from core.state.add import AddTemplate
from core.db.functions import ActionORM


router = Router()


@router.message(IsAdmin(), Command('admin'))
async def admin_login(message: types.Message):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text='✅ Добавить шаблон'),
            types.KeyboardButton(text='❌ Удалить шаблон'),
        ],
    ], resize_keyboard=True)
    await message.answer('Вы успешно зашли в админ-панель!', reply_markup=keyboard)


@router.message(IsAdmin(), F.text == "✅ Добавить шаблон")
async def show_type_holidays(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ф-я вывода праздников"""
    msg_txt = "Выбери праздник для которого необходимо создать шаблон"
    holidays = await ActionORM.get_holidays()
    
    builder = InlineKeyboardBuilder()
    for holiday in holidays:
        builder.button(text=holiday['name'], callback_data=HolidayCallback(holiday=holiday['name'], id=holiday['id']).pack())
    builder.adjust(2)

    await bot.send_photo(
        chat_id=message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=builder.as_markup())
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await state.set_state(AddTemplate.get_holiday_id)


@router.callback_query(IsAdmin(), StateFilter(AddTemplate.get_holiday_id), F.data.startswith('holiday:'))
async def call_type_holiday(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я обработки выбора шаблона"""
    callback_data = callback.data
    print(callback_data)
    await state.update_data(holiday_id=callback_data)
    txt = """
    Напишите шаблон для праздника\n
    Доступны следующие параметры:
    {firstname} - Имя поздравляемого
    {lastname} - Фамилия поздравляемого
    {patronymic} - Отчество поздравляемого
    {sender} - Данные поздравителя\n
    Пример: Привет {firstname} {patronymic}, поздравляю тебя с твоим днем!
    """
    msg_txt = dedent(txt)
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=ReplyKeyboardRemove())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(AddTemplate.get_template_text)


@router.message(IsAdmin(), StateFilter(AddTemplate.get_template_text))
async def get_template_text(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ф-я для добавления шаблонов поздравлений"""
    text = message.text
    # print(text)
    if text is not None and text.strip() != '':
        if len(text) < 280:
            await state.update_data(template_text=text)
            data = await state.get_data()
            print(data)
            data_holiday = data.get('holiday_id')
            data_holiday_unpacked = HolidayCallback.unpack(data_holiday)
            holiday = data_holiday_unpacked.holiday
            template_text = data.get('template_text')

            builder = InlineKeyboardBuilder()
            builder.button(text="✅ Да", callback_data="да")
            builder.button(text="❌ Нет", callback_data="нет")
            builder.adjust(2)

            txt = f"""
                Вы действительно хотите добавить шаблон поздравления 
                ***
                {template_text}
                ***
                Для праздника {holiday}?
            """
            msg_txt = dedent(txt)
            await bot.send_message(chat_id=message.chat.id, text=msg_txt, reply_markup=builder.as_markup())
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await state.set_state(AddTemplate.confirm_template_text)
        else:
            bot.send_message(chat_id=message.chat.id, text="Текст шаблона первышает ограничения в 280 символов")
    else:
        bot.send_message(chat_id=message.chat.id, text="Текст шаблона не может быть пустым")


@router.callback_query(IsAdmin(), StateFilter(AddTemplate.confirm_template_text), F.data.lower() == "да")
async def yes_confirm_template_text(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я обработки при подтверждении добавления шаблона праздника"""
    data = await state.get_data()
    data_holiday = data.get('holiday_id')
    data_holiday_unpacked = HolidayCallback.unpack(data_holiday)
    holiday_id = data_holiday_unpacked.id
    template_text = data.get('template_text')
    # Вызов функции добавления шаблона в БД и передача параметра
    result = await ActionORM.add_template_for_holiday(holiday_id=holiday_id, pattern_text=template_text)
    await callback.answer()
    await bot.send_message(chat_id=callback.message.chat.id, text=result)
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@router.callback_query(IsAdmin(), StateFilter(AddTemplate.confirm_template_text), F.data.lower() == "нет")
async def no_confirm_template_text(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я обработки при отклонении добавления шаблона праздника"""
    pass


@router.callback_query(IsAdmin(), F.text == "❌ Удалить шаблон")
async def delete_temlate(id) -> None:
    """Ф-я для удаления шаблонов поздравлений"""
    pass