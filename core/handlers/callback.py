from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext


from core.state.dialog import FSMDialog
from core.keyboard.keyboard import group_action_ikb, users_action_ikb
from aiogram.types import FSInputFile


router = Router()

# Ф-я отображения пользователей
@router.callback_query(F.text=="Показать пользователей")
async def show_users( callback: CallbackQuery ) -> None:
  msg_txt = "Управление пользователями"
  await callback.message.answer(msg_txt, reply_markup=group_action_ikb())
  await callback.answer()

# Ф-я отображения групп
@router.callback_query(F.data=="btn_text:Показать пользователей")
async def show_groups( callback: CallbackQuery ) -> None:
  msg_txt = "Управление группами"
  await callback.message.answer(msg_txt, reply_markup=users_action_ikb())
  await callback.answer()