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
from core.handlers.factories import HolidayCallback, HolidayTemplateCallback
from core.state.temlate import ActionTemplate
from core.db.functions import ActionORM
from core.utils.workstr import StrRegular


router = Router()


@router.message(IsAdmin(), Command('admin'))
async def admin_login(message: types.Message, state: FSMContext) -> None:
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            types.KeyboardButton(text='✅ Добавить праздник'),
            types.KeyboardButton(text='❌ Удалить праздник'),
        ],
        [
            types.KeyboardButton(text='✅ Добавить шаблон'),
            types.KeyboardButton(text='❌ Удалить шаблон'),
        ],
    ], resize_keyboard=True)
    await message.answer('Вы успешно зашли в админ-панель!', reply_markup=keyboard)


@router.message(IsAdmin(), F.text.in_({"❌ Удалить праздник", "✅ Добавить шаблон", "❌ Удалить шаблон"}))
async def menu_processing(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ф-я вывода праздников"""
    try:
        holidays = await ActionORM.get_holidays()
        
        builder = InlineKeyboardBuilder()
        for holiday in holidays:
            builder.button(text=holiday['name'], callback_data=HolidayCallback(holiday=holiday['name'], id=holiday['id']).pack())
        builder.adjust(2)

        if message.text == "❌ Удалить праздник":
            await state.update_data(action=message.text)
            msg_txt = "Выберите праздник который хотите удалить"
            await bot.send_photo(
                chat_id=message.chat.id,
                photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
                caption=msg_txt,
                reply_markup=builder.as_markup())
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await state.set_state(ActionTemplate.get_holiday)

        if message.text == "✅ Добавить шаблон":
            await state.update_data(action=message.text)
            # data = await state.get_data()
            # print(data)
            msg_txt = "Выберите праздник для которого необходимо создать шаблон"
            await bot.send_photo(
                chat_id=message.chat.id,
                photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
                caption=msg_txt,
                reply_markup=builder.as_markup())
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await state.set_state(ActionTemplate.get_holiday)

        if message.text == "❌ Удалить шаблон":
            await state.update_data(action=message.text)
            # data = await state.get_data()
            # print(data)
            msg_txt = "Выберите праздник для которого необходимо удалить шаблон"
            await bot.send_photo(
                chat_id=message.chat.id,
                photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
                caption=msg_txt,
                reply_markup=builder.as_markup())
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await state.set_state(ActionTemplate.get_holiday)
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=message.chat.id, text=f"Ошибка в обработке данных {e}")


@router.callback_query(IsAdmin(), StateFilter(ActionTemplate.get_holiday), F.data.startswith('holiday:'))
async def call_type_holiday(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я обработки выбора шаблона"""
    try:
        data = await state.get_data()
        # print(data)
        action = data.get("action")

        if action == "❌ Удалить праздник":
            await state.update_data(holiday=callback.data)
            data = await state.get_data()
            holiday = data.get("holiday")
            holiday_unpacked = HolidayCallback.unpack(holiday)
            holiday_name = holiday_unpacked.holiday
            holiday_id = holiday_unpacked.id

            builder = InlineKeyboardBuilder()
            builder.button(text="✅ Да", callback_data="да")
            builder.button(text="❌ Нет", callback_data="нет")
            builder.adjust(2)

            msg_txt = f"Вы действительно хотите удалить праздник {holiday_name}"
            msg_txt = dedent(msg_txt)
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=msg_txt,
                reply_markup=builder.as_markup())
            await callback.answer()
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

        if action == "✅ Добавить шаблон":
            callback_data = callback.data
            # print(callback_data)
            await state.update_data(holiday=callback_data)
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
            await state.set_state(ActionTemplate.get_template)

        if action == "❌ Удалить шаблон":
            await state.update_data(holiday=callback.data)
            data = await state.get_data()
            holiday = data.get("holiday")
            holiday_unpacked = HolidayCallback.unpack(holiday)
            holiday_id = holiday_unpacked.id

            templates = await ActionORM.get_templates(holiday_id)

            builder = InlineKeyboardBuilder()
            for template in templates:
                builder.button(text=f"Шаблон {str(template['id'])}", callback_data=HolidayTemplateCallback(template=f"Шаблон {str(template['id'])}", id=template['id'], level=1).pack())
            builder.adjust(2)

            msg_txt = "Выберите шаблон который хотите удалить"

            await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
                caption=msg_txt,
                reply_markup=builder.as_markup())
            await callback.answer()
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await state.set_state(ActionTemplate.get_template)
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=callback.message.chat.id, text=f"Ошибка в обработке данных {e}")


@router.message(IsAdmin(), F.text == "✅ Добавить праздник")
async def add_holiday(message: Message, bot: Bot, state: FSMContext) -> None:
    """Добавлить шаблон поздравления"""
    try:
        msg_txt = "Напишите название праздника"
        await bot.send_message(chat_id=message.chat.id, text=msg_txt)
        await state.set_state(ActionTemplate.get_holiday)
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=message.chat.id, text=f"Ошибка в обработке данных {e}")


@router.message(IsAdmin(), ActionTemplate.get_holiday)
async def get_new_holiday(message: Message, bot: Bot, state: FSMContext) -> None:
    """Добавить новый праздник"""
    try:
        name_holiday = message.text
        if name_holiday is not None and name_holiday.strip() != '':
            await state.update_data(new_holiday=name_holiday)
            result = await ActionORM.add_holiday(name_holiday=name_holiday)
            # msg_txt = "Праздник добавлен"
            await bot.send_message(chat_id=message.chat.id, text=f"{result}")
        else:
            msg_txt = "Введите название праздника"
            await bot.send_message(message.chat.id, msg_txt)
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=message.chat.id, text=f"Ошибка в обработке данных {e}")


@router.callback_query(IsAdmin(), StateFilter(ActionTemplate.get_holiday))
async def delete_holiday(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """ Ф-я удаления праздника """
    try:
        data = await state.get_data()
        # print(data)
        action = data.get("action")

        if action == "❌ Удалить праздник":
            if callback.data.lower() == "да":
                holiday = data.get("holiday")
                holiday_unpacked = HolidayCallback.unpack(holiday)
                holiday_id = holiday_unpacked.id

                result = await ActionORM.delete_holiday(holiday_id)
                await callback.answer()
                await bot.send_message(chat_id=callback.message.chat.id, text=result)
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
                await state.clear()

            if callback.data.lower() == "нет":
                msg_txt = "Удаление праздника отменено :D"
                await callback.answer()
                await bot.send_message(chat_id=callback.message.chat.id, text=msg_txt)
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
                await state.clear()
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=callback.message.chat.id, text=f"Ошибка в обработке данных {e}")


@router.message(IsAdmin(), StateFilter(ActionTemplate.get_template))
async def add_template_text(message: Message, bot: Bot, state: FSMContext) -> None:
    """Ф-я для добавления шаблонов поздравлений"""
    try:
        data = await state.get_data()
        # print(data)
        action = data.get("action")
        text = message.text
        # print(text)
        if action == "✅ Добавить шаблон":
            if text is not None and text.strip() != '':
                if len(text) < 280:
                    await state.update_data(template_text=text)
                    data = await state.get_data()
                    print(data)
                    data_holiday = data.get('holiday')
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
                    await state.set_state(ActionTemplate.confirm_template_text)
                else:
                    bot.send_message(chat_id=message.chat.id, text="Текст шаблона первышает ограничения в 280 символов")
            else:
                bot.send_message(chat_id=message.chat.id, text="Текст шаблона не может быть пустым")
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=message.chat.id, text=f"Ошибка в обработке данных {e}")


@router.callback_query(IsAdmin(), StateFilter(ActionTemplate.get_template))
async def delete_template(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я для удаления шаблонов поздравлений"""
    try:
        states = await state.get_state()
        print(states)

        data = await state.get_data()
        action = data.get('action')
        # print(action)
        if action == "❌ Удалить шаблон":
            data_holiday = data.get('holiday')
            data_holiday_unpacked = HolidayCallback.unpack(data_holiday)
            holiday = data_holiday_unpacked.holiday

            unpacked_callback = HolidayTemplateCallback.unpack(callback.data)
            await state.update_data(template_id=unpacked_callback.id)
            template_text = await ActionORM.get_template(unpacked_callback.id)

            if template_text and isinstance(template_text, str):
                template_txt = template_text
                await state.update_data(confirm_template=template_text)
            else:
                template_txt = "Текст шаблона не найден."

            builder = InlineKeyboardBuilder()
            builder.button(text="✅ Да", callback_data="да")
            builder.button(text="❌ Нет", callback_data="нет")
            builder.adjust(2)

            txt = f"""
                Вы действительно хотите удалить шаблон поздравления 
                ***
                {template_txt}
                ***
                Для праздника {holiday}?
            """
            msg_txt = dedent(txt)
            await bot.send_message(chat_id=callback.message.chat.id, text=msg_txt, reply_markup=builder.as_markup())
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await state.set_state(ActionTemplate.confirm_template_text)
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=callback.message.chat.id, text=f"Ошибка в обработке данных {e}")


@router.callback_query(IsAdmin(), StateFilter(ActionTemplate.confirm_template_text), F.data.lower() == "да")
async def yes_add_or_delete_template_text(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я обработки при подтверждении добавления/удаления шаблона праздника"""
    try:
        states = await state.get_state()
        print(states)

        data = await state.get_data()
        print(data)
        action = data.get('action')
        # print(action)

        data_holiday = data.get('holiday')
        data_holiday_unpacked = HolidayCallback.unpack(data_holiday)
        holiday_id = data_holiday_unpacked.id
        template_id = data.get('template_id')
        # print(holiday_id)
        template_text = data.get('template_text')
        # print(template_text)

        if action == "✅ Добавить шаблон":
            result = await ActionORM.add_template_for_holiday(holiday_id=holiday_id, pattern_text=template_text)
            await callback.answer()
            await bot.send_message(chat_id=callback.message.chat.id, text=result)
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await state.clear()

        if action == "❌ Удалить шаблон":
            result = await ActionORM.delete_template(pattern_id=template_id)
            print(result)
            await callback.answer()
            await bot.send_message(chat_id=callback.message.chat.id, text=result)
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await state.clear()
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=callback.message.chat.id, text=f"Ошибка в обработке данных {e}")


@router.callback_query(IsAdmin(), StateFilter(ActionTemplate.confirm_template_text), F.data.lower() == "нет")
async def no_add_or_delete_template_text(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я обработки при отклонении добавления/удаления шаблона праздника"""
    try:
        data = await state.get_data()
        action = data.get('action')
        # print(action)
        if action == "✅ Добавить шаблон":
            msg_txt = "Создание шаблона отменено"
            await bot.send_message(chat_id=callback.message.chat.id, text=msg_txt)
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            state.clear()

        if action == "❌ Удалить шаблон":
            msg_txt = "Удаление шаблона отменено))"
            await callback.answer()
            await bot.send_message(chat_id=callback.message.chat.id, text=msg_txt)
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            state.clear()
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")
        await bot.send_message(chat=callback.message.chat.id, text=f"Ошибка в обработке данных {e}")
