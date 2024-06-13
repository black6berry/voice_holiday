import os
import re
from main import BASE_DIR
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from core.keyboard.keyboard import  choose_and_back_ikb, main_menu_ikb
from core.handlers.factories import MyCallback, HolidayCallback, HolidayTemplateCallback
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.state.menu import MenuState
from core.db.functions import ActionORM
from aiogram.filters import StateFilter
from core.keyboard import text_kb
from aiogram.filters.callback_data import CallbackData
from core.utils.workstr import StrRegular
from services import gradio
from core.filters.is_admin import IsAdmin


router = Router()


@router.callback_query(StateFilter(MenuState.main_menu), F.data.lower() == "выбрать праздник")
async def show_holiays(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я отображения праздников"""
    # if callback.data == "назад":
    #     pass
    # else:
    await state.update_data(main_menu=callback.data)

    msg_txt = "Выбери праздник или напиши свой текст поздравления"
    holidays = await ActionORM.get_holidays()

    builder = InlineKeyboardBuilder()
    for holiday in holidays:
        builder.button(text=holiday['name'], callback_data=HolidayCallback(holiday=holiday['name'], id=holiday['id']).pack())
    builder.adjust(2)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text=text_kb.create_holiday_yourself, callback_data="Свой шаблон")
    builder.attach(another_builder)

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=builder.as_markup())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(MenuState.get_template)


@router.callback_query(StateFilter(MenuState.get_template), F.data.lower() == "назад")
async def go_back_show_holidays(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Перейти в выбор праздника НАЗАД"""
    msg_txt = "Выбери праздник или напиши свой текст поздравления"
    holidays = await ActionORM.get_holidays()

    builder = InlineKeyboardBuilder()
    for holiday in holidays:
        builder.button(text=holiday['name'], callback_data=HolidayCallback(holiday=holiday['name'], id=holiday['id']).pack())
    builder.adjust(2)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text=text_kb.create_holiday_yourself, callback_data="Свой шаблон")
    builder.attach(another_builder)

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=builder.as_markup())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(MenuState.get_holiday)


@router.callback_query(StateFilter(MenuState.get_template), F.data.startswith("holiday"))
async def show_templates(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я отображения шаблонов праздника"""
    await state.update_data(holiday=callback.data)
    print(callback.data)

    state0 = await state.get_state()
    print(state0)
    data = await state.get_data()
    print(data)

    # if callback.data == "назад":
    #     pass
    #     # await callback.answer()
    #     # await show_holiays(callback, bot, state)
    # else:
    # await state.update_data(holiday=callback.data)
    # callback_unpacked = HolidayCallback.unpack(callback.data)

    holiday = data.get("holiday")
    print(holiday)
    holiday_unpacked = HolidayCallback.unpack(holiday)
    print(holiday_unpacked)
    holiday_id = holiday_unpacked.id
    
    templates = await ActionORM.get_templates(holiday_id)

    builder = InlineKeyboardBuilder()
    for template in templates:
        builder.button(text=f"Шаблон {str(template['id'])}", callback_data=HolidayTemplateCallback(template=f"Шаблон {str(template['id'])}", id=template['id'], level=1).pack())
    builder.adjust(2)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text=text_kb.menu_back, callback_data="назад")
    builder.attach(another_builder)

    msg_txt = "Выбери шаблон поздравления"

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=builder.as_markup())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(MenuState.get_template_text)


@router.callback_query(StateFilter(MenuState.get_template_text), F.data.lower() == "назад")
async def go_back_show_templates(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Перейти в выбор шаблона для праздника"""
    state = await state.get_state()
    print(state)
    data = await state.get_data()
    print(data)

    await state.update_data(holiday=callback.data)

    callback_unpacked = HolidayCallback.unpack(callback.data)
    holiday_id = callback_unpacked.id

    data = await state.get_data()
    print(data)
    templates = await ActionORM.get_templates(holiday_id)

    builder = InlineKeyboardBuilder()
    for template in templates:
        builder.button(text=f"Шаблон {str(template['id'])}", callback_data=HolidayTemplateCallback(template=f"Шаблон {str(template['id'])}", id=template['id'], level=1).pack())
    builder.adjust(2)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text=text_kb.menu_back, callback_data="назад")
    builder.attach(another_builder)

    msg_txt = "Выбери шаблон поздравления"

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=builder.as_markup())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(MenuState.get_template)



@router.callback_query(StateFilter(MenuState.get_template_text), F.data.startswith('holiday_template'))
async def show_template_txt(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Ф-я отображения текста шаблона"""
    unpacked_callback = HolidayTemplateCallback.unpack(callback.data)
    template_text = await ActionORM.get_template(unpacked_callback.id)

    if template_text and isinstance(template_text[0][0], str):
        template_txt = template_text[0][0]
        await state.update_data(confirm_template=template_text)
    else:
        template_txt = "Текст шаблона не найден."

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=template_txt,
        reply_markup=choose_and_back_ikb())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(MenuState.get_voice)


# @router.callback_query(StateFilter(MenuState.get_voice), F.data.lower() == "назад")
# async def go_back_show_templates(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
#     """Перейти в выбор праздника НАЗАД"""
#     await state.set_state(MenuState.get_template_text)
#     await show_templates(callback, bot, state)


@router.callback_query(StateFilter(MenuState.get_voice), F.data.lower() == "выбрать")
async def show_voice_dictors(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Перейти в выбор праздничного шаблона НАЗАД"""
    data = await state.get_data()
    print(data)
    print(callback.data)
    await state.update_data(voice=callback.data)

    voices_dictors = ["Anya", "Marat", "Polina", "Putin", "Putin2", "Roma", "Sergey", "Tom"]

    builder = InlineKeyboardBuilder()
    for voice in voices_dictors:
        builder.button(text=f"{voice}", callback_data=f"dictors:{voice}")
    builder.adjust(2)

    another_builder = InlineKeyboardBuilder()
    another_builder.button(text=text_kb.menu_back, callback_data="назад")
    builder.attach(another_builder)
    msg_txt = "Выберите голос диктора"

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=builder.as_markup())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(MenuState.confirm_voice)


@router.callback_query(StateFilter(MenuState.confirm_voice), F.data.lower() == "назад")
async def go_back_show_voice_dictors(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Перейти в выбор праздничного шаблона НАЗАД"""
    await state.set_state(MenuState.get_voice)
    pass


@router.callback_query(StateFilter(MenuState.confirm_voice), F.data.startswith("dictors"))
async def confirm_voice(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Подтвердить выбранный голос"""
    dictor = callback.data.replace('dictors:', '')
    print(dictor)
    await state.update_data(dictor=dictor)
    
    file_name = f"{dictor}.mp3"
    file_path = os.path.join(BASE_DIR, 'voices', file_name)

    if not os.path.exists(file_path):
        await callback.message.answer(f"Файл {file_name} не найден.")
        return
    file = FSInputFile(file_path, file_name)

    await bot.send_audio(chat_id=callback.message.chat.id, audio=file, caption="Выбрать этот голос для поздравления? ", reply_markup=choose_and_back_ikb())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(MenuState.get_firstname)


@router.callback_query(StateFilter(MenuState.get_firstname), F.data.lower() == "выбрать")
async def get_firstname_user(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    print(callback.data)
    """Обработка callback кнопки"""
    msg_txt = "Введите имя человека которого собираетесь поздравить"
    await bot.send_message(callback.message.chat.id, msg_txt)
    await callback.answer()
    await state.set_state(MenuState.get_firstname)


@router.message(StateFilter(MenuState.get_firstname))
async def get_firstname_user_msg(message: Message, bot: Bot, state: FSMContext):
    """ 
        Получение имени пользователя которого поздравляем 
        Обработка message
    """
    try:
        firstname = message.text
        result = await StrRegular.contains_only_non_digits(message.text)
        if result is not False:
            # print(firstname)
            await state.update_data(firstname=firstname)
            msg_txt = "Введите Фамилию человека которого собираетесь поздравить"
            await bot.send_message(message.chat.id, msg_txt)
            await state.set_state(MenuState.get_lastname)
        else: 
            msg_txt = "Введи имя без лишних символов и чисел :D"
            await bot.send_message(message.chat.id, msg_txt)
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")


@router.message(StateFilter(MenuState.get_lastname))
async def get_lastname_user(message: Message, bot: Bot, state: FSMContext) -> None:
    """ Получение фамилии пользователя которого поздравляем """
    try:
        lastname = message.text 
        result = await StrRegular.contains_only_non_digits(message.text)
        if result is not False:
            # print(lastname)
            await state.update_data(lastname=lastname)
            msg_txt = "Введите отчество человека которого собираетесь поздравить"
            await bot.send_message(message.chat.id, msg_txt)
            await state.set_state(MenuState.get_patronymic)
        else: 
            msg_txt = "Введи фамилию без лишних символов и чисел :D"
            await bot.send_message(message.chat.id, msg_txt)
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")


@router.message(StateFilter(MenuState.get_patronymic))
async def get_patronymic_user(message: Message, bot: Bot, state: FSMContext) -> None:
    """ Получение отчества пользователя которого поздравляем """
    try:
        patronymic = message.text
        result = await StrRegular.contains_only_non_digits(message.text)
        if result is not False:
            # print(patronymic)
            await state.update_data(patronymic=patronymic)
            msg_txt = "Введите данные поздравляющего"
            await bot.send_message(message.chat.id, msg_txt)
            await state.set_state(MenuState.get_sender)
        else: 
            msg_txt = "Введи фамилию без лишних символов и чисел :D"
            await bot.send_message(message.chat.id, msg_txt)
    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")


@router.message(StateFilter(MenuState.get_sender))
async def get_sender_data_user(message: Message, bot: Bot, state: FSMContext) -> None:
    """ Получение данных поздравляющего """
    try:
        sender = message.text
        result = await StrRegular.contains_only_non_digits(message.text)
        
        if result is not False:
            
            # print(sender)
            await state.update_data(sender=sender)
            # msg_txt = "Данные записаны, ваш запрос отправлен, ожидайте проверки модератором"
            msg_txt = " Идет генерация запроса..."
            await bot.send_message(message.chat.id, msg_txt)

            data = await state.get_data()
            model = data.get('dictor')
            text = data.get('confirm_template')[0][0]
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            patronymic = data.get('patronymic')
            sender = data.get('sender')
            # Склейка шаблона с параметрами из FSM MenuState
            text_template = text.format(firstname=firstname, lastname=lastname, patronymic=patronymic, sender=sender)
            ### Отправка API запроса на сервер для получения mp3 файла ###
            result = await gradio.send_request_gradio(model_name=model, tts_text=text_template)

            print(f"Result: {result}")
            mp3_path_result = result['mp3_path']
            mp3_filename = os.path.basename(mp3_path_result)
            mp3_file = FSInputFile(mp3_path_result, mp3_filename)

            wav_path_result = result['wav_path']
            wav_filename = os.path.basename(wav_path_result)
            wav_file = FSInputFile(wav_path_result, wav_filename)
            
            await bot.send_audio(chat_id=message.chat.id, audio=mp3_file, caption="Вариант 1")
            await bot.send_audio(chat_id=message.chat.id, audio=wav_file, caption="Вариант 2")

        else:
            msg_txt = "Имя отправителя должно быть строкой :D"
            await bot.send_message(message.chat.id, msg_txt)

    except ValueError as e:
        print(f"Ошибка в обработке данных {e}")


@router.message(StateFilter(MenuState.get_sender))
async def get_sender_data_user_answer_for_message(message: Message, bot: Bot, state: FSMContext) -> None:
    """ Получение данных поздравляющего """
    msg_txt = " Идет генерация запроса..."
    await bot.send_message(message.chat.id, msg_txt)


@router.callback_query(MyCallback.filter(F.text.lower().in_({"главное меню", "назад"})), StateFilter(MenuState.main_menu))
async def go_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Обработка нажатия кнопки назад из состояния 'Показать поздравления'"""
    msg_txt = " Voice Holiday - Сервис для поздравлений пользователей по системе радиовещания :D "
    await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=main_menu_ikb())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await state.set_state(MenuState.main_menu)