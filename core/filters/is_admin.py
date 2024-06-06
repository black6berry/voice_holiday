from aiogram.types import Message
from aiogram.filters import Filter
from core.config.config import ADMIN_ID_LIST

class IsAdmin(Filter):

    """Кастомный фильтр для проверки на админа"""
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        is_admin = user_id in ADMIN_ID_LIST
        print(is_admin)
        if is_admin is False:
            await message.answer(text="Данный функционал для вас недоступен,\nтак как вы не являетесь администратором :D")
        return is_admin