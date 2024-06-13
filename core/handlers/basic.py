from aiogram.filters import CommandStart, Command 
from aiogram import F, Router
from aiogram.types import Message
from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from core.state.menu import MenuState
from aiogram.filters import StateFilter

from core.keyboard.keyboard import main_menu_ikb


router = Router()


@router.message(CommandStart())
@router.message(StateFilter('*'), F.text.lower().in_({"главное меню", "меню", "начать"}))
async def get_start(message: Message, bot: Bot, state: FSMContext) -> None:
    """ Общая команда старта """  
    msg_txt = "Voice Holiday - Сервис для поздравлений пользователей по системе радиовещания :D"
    await bot.send_photo(chat_id=message.chat.id, photo='AgACAgIAAxkBAAM5Zg8ZGlMXFVPmCpCP-rfk3DstbKEAAtHaMRsqD3hIhX3bOM8WgioBAAMCAAN5AAM0BA', caption=msg_txt, reply_markup=main_menu_ikb())
    await state.set_state(MenuState.get_holiday)

@router.message(Command("help"))
async def get_help_me(message: Message, bot: Bot) -> None:
    """ Команда помощи """
    msg_txt = "Я бот который поздравляет людей с их днем рождения.\nВведи команду /start чтобы начать.\nИли можешь отправить мне сообщение: начать, меню, главное меню"
    await bot.send_message(chat_id=message.chat.id, text=msg_txt)