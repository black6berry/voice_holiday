from aiogram.types import CallbackQuery
from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from core.keyboard.keyboard import  main_menu_admin_ikb, users_action_ikb
from core.keyboard.keyboard import MyCallback, groups_ikb, back_ikb
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.state.menu import MenuState
from core.db.functions import ActionORM
from aiogram.filters import StateFilter



router = Router()

@router.callback_query(StateFilter(MenuState.main_menu), MyCallback.filter(F.btn_txt.lower() == "показать группы"))
async def show_groups(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я отображения групп"""
    await state.set_state(MenuState.menu_step2) # устанавливаем состоянние

    groups = ActionORM.get_groups() # получаем список групп
    print(groups)
    if groups is not None:

        builder = InlineKeyboardBuilder()
        groups_count = 0

        for group in groups:
            builder.button(text=f"{group['Name']}", callback_data=f"group_{group['Name']}_{group['ID']}")
            groups_count += 1
        builder.adjust(3, 3)
        msg_txt = f"Количество групп - {groups_count}"
    else:
        msg_txt = "Нет групп"

    builder.attach(InlineKeyboardBuilder.from_markup(groups_ikb))

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=builder.as_markup())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@router.callback_query(StateFilter(MenuState.menu_step2), F.data.startswith("group_"))
async def show_group(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """ф-я обработки выбора группы"""
    await state.set_state(MenuState.menu_step3)
    group_name = callback.data.split("_")[1]
    msg_txt = f"Выбрана группа - {group_name}"

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=back_ikb)
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


@router.callback_query(MyCallback.filter(F.btn_txt.lower() == "показать пользователей"))
async def show_users(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я отображения пользователей"""
    await state.set_state(MenuState.menu_step3)
    users = ActionORM.get_users()

    if users is not None:
        msg_txt = "ID | Name\n"
        for user in users:
            msg_txt += f"{user['ID']} - {user['Name']}\n"
    else:
        msg_txt = "Нет групп"

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=users_action_ikb())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@router.callback_query(MyCallback.filter(F.btn_txt.lower() == "главное меню"))
async def show_main_menu(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    """Ф-я возврата в главное меню"""
    await state.set_state(MenuState.main_menu)

    msg_txt = "Главное меню"

    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA',
        caption=msg_txt,
        reply_markup=main_menu_admin_ikb())
    await callback.answer()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)

