from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    search_edition_isnb = State()
    search_work_name = State()
    search_author_name = State()