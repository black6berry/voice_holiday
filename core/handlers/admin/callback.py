from aiogram import Bot, Router, F
from aiogram.filters import Command
from core.filters.is_admin import IsAdmin
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

router = Router()


@router.message(IsAdmin(), Command('admin'))
async def admin_login(message: types.Message):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text='✅ Добавить шаблон')],
        [types.KeyboardButton(text='❌ Удалить шаблон')]
    ], resize_keyboard=True)
    await message.answer('Вы успешно зашли в админ-панель!', reply_markup=keyboard)


@router.callback_query(IsAdmin(), F.text == "✅ Добавить шаблон")
async def add_temlate(holiday_id, text) -> None:
    """Ф-я для добавления шаблонов поздравлений"""
    pass


@router.callback_query(IsAdmin(), F.text == "❌ Удалить шаблон")
async def delete_temlate(id) -> None:
    """Ф-я для удаления шаблонов поздравлений"""
    pass