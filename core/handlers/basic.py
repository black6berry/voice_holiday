from aiogram.filters import CommandStart, Command 
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from core.state.menu import MenuState
from aiogram.filters import StateFilter

from core.keyboard.keyboard import main_menu_admin_ikb
from aiogram.types import FSInputFile


router = Router()

@router.message(F.photo)
async def upload_main_menu_photo(message: Message) -> None:
    """ Ф-я Загрузка фоток """
    photo_data = message.photo[-1]
    await message.answer(f'{photo_data}')

@router.message(StateFilter('*'), F.btn_txt.lower() == "главное меню")
@router.message(CommandStart())
async def get_start(message: Message, bot: Bot, state: FSMContext) -> None:
    """ Общая команда старта """  
    await state.set_state(MenuState.main_menu)
    msg_txt = " Voice Holiday - Сервис для поздравлений пользователей по системе радиовещания :D "
    await bot.send_photo(chat_id=message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=main_menu_admin_ikb())

@router.message(Command("help"))
async def get_help_me(message: Message, bot: Bot) -> None:
    """ Команда помощи """
    msg_txt = "Я бот который поздравляет людей с их днем рождения.\nВведи команду /start чтобы начать"
    await bot.send_message(chat_id=message.chat.id, text=msg_txt)