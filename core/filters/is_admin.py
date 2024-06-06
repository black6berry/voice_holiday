from aiogram.types import Message
from aiogram.filters import Filter
from core.config.config import ADMIN_ID_LIST

class IsAdmin(Filter):
    """Кастомный фильтр для проверки на админа"""
    async def check(self, message: Message):
        return message.from_user.id in ADMIN_ID_LIST