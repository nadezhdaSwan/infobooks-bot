from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.search_states import Form
from aiogram.fsm.context import FSMContext

from create_bot import logger

from bibliosites import fantlab
from db.edition_class import Edition

from handlers.common import send_info, pagination

search_edition_isnb_router = Router()

@search_edition_isnb_router.message(F.text == 'search_edition_isnb')
async def cmd_search_edition_isnb(message: Message, state: FSMContext):
    logger.info('Command search_edition_isnb')
    #await message.answer('''Enter isnb to search the edition of book:''')
    await message.answer('''Введите isnb для поиска издания книги:''')
    await state.set_state(Form.search_edition_isnb)

@search_edition_isnb_router.message(Form.search_edition_isnb)
async def send_info_book_isnb(message: Message, state: FSMContext):
    await state.update_data(search_edition_isnb=message.text)
    user_data = await state.get_data()

    #edition = send_info(user_data['search_edition_isnb'], fantlab.get_info_about_edition_from_isnb, Edition)
    editions = pagination(user_data['search_edition_isnb'], Edition)

    await message.answer(
        text=str(editions),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()