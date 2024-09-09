from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.search_states import Form
from aiogram.fsm.context import FSMContext

from create_bot import logger

from bibliosites import fantlab
from db.author_class import Author

from handlers.common import send_info

search_author_name_router = Router()

@search_author_name_router.message(F.text == 'search_author_name')
async def cmd_search_author_name(message: Message, state: FSMContext):
    logger.info('Command search_author_name')
    #await message.answer('''Enter author name:''')
    await message.answer('''Введите имя автора:''')
    await state.set_state(Form.search_author_name)

@search_author_name_router.message(Form.search_author_name)
async def send_info_book_isnb(message: Message, state: FSMContext):
    await state.update_data(search_author_name=message.text)
    user_data = await state.get_data()

    author = send_info(user_data['search_author_name'], fantlab.get_info_about_author_from_name, Author)

    await message.answer(
        text=str(author),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


