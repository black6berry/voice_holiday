from aiogram.fsm.state import State, StatesGroup

class FSMDialog(StatesGroup):
  user_firstname = State()
  user_lastname = State() 
  datebirthday = State()
  student_group = State()
  student_group_id = State()

  async def clear(self) -> None:
    await self.set_state(state=None)
    await self.set_data({})