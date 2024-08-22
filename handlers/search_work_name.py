from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.search_states import Form
from aiogram.fsm.context import FSMContext

from create_bot import logger

from bibliosites import fantlab
from db.work_class import Work

from handlers.common import send_info

search_work_name_router = Router()

@search_work_name_router.message(Command('search_work_name'))
async def cmd_search_work_name(message: Message, state: FSMContext):
    logger.info('Command search_work_name')
    await message.answer('''Enter work name:''')
    await state.set_state(Form.search_work_name)

@search_work_name_router.message(Form.search_work_name)
async def send_info_book_isnb(message: Message, state: FSMContext):
    await state.update_data(search_work_name=message.text)
    user_data = await state.get_data()

    work = send_info(user_data['search_work_name'], fantlab.get_info_about_work_from_name, Work)

    await message.answer(
        text=str(work),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()