from mailbox import Message
from aiogram.types import CallbackQuery
from aiogram import Bot, Router, F, types
from aiogram.fsm.context import FSMContext
from core.handlers.basic import get_start
from core.keyboard.keyboard import main_menu_admin_ikb, users_action_ikb
from core.keyboard.keyboard import MyCallback, back_ikb
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from core.state.menu import MenuState
from core.db.functions import ActionORM
from aiogram.filters import StateFilter
from aiogram_inline_paginations.paginator import Paginator
from core.keyboard import text_kb


router = Router()

@router.callback_query(MyCallback.filter(F.btn_txt.lower() == "показать пользователей"))
async def show_users(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я отображения пользователей"""
    await state.set_state(MenuState.menu_step2)
    users = ActionORM.get_users()

    if users is not None:

        builder = InlineKeyboardBuilder()
        groups_count = 0

        for user in users:
            builder.button(text=f"{user['firstname']} {user['lastname']}", callback_data=f"user_{user['firstname']}_{user['lastname']}")
            groups_count += 1
        builder.adjust(4, 4)

        paginator = Paginator(data=builder.as_markup(), size=8, page_separator='|')
        
        msg_txt = f"Количество пользователей - {groups_count}"
    else:
        msg_txt = "Нет пользователей"

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=paginator())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@router.callback_query(StateFilter(MenuState.main_menu), MyCallback.filter(F.btn_txt.lower() == "тексты поздравлений"))
async def show_congratulations(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я отображения текстов поздравлений"""
    await state.set_state(MenuState.menu_step2)
    birthday_texts = ActionORM.get_congratulations()

    if birthday_texts is not None:
        msg_txt = "ID | Name\n"
        for text in birthday_texts:
            msg_txt += f"{text['ID']} - {text['Name']}\n"
    else:
        msg_txt = "Нет текстов поздравлений"

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=back_ikb)
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@router.callback_query(MyCallback.filter(F.btn_txt.lower() == "главное меню"), StateFilter(MenuState.menu_step2))
@router.callback_query(MyCallback.filter(F.btn_txt.lower() == "назад"), StateFilter(MenuState.menu_step2))
async def go_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Обработка нажатия кнопки назад из состояния 'Показать поздравления'"""
    await state.set_state(MenuState.main_menu)
    msg_txt = " Voice Holiday - Сервис для поздравлений пользователей по системе радиовещания :D "
    await bot.send_photo(chat_id=callback.message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=main_menu_admin_ikb())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
