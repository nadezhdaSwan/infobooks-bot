from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.search_states import Form
from aiogram.fsm.context import FSMContext

from create_bot import logger

from bibliosites import fantlab
from db.edition_class import Edition


search_edition_isnb_router = Router()

@search_edition_isnb_router.message(Command('search_edition_isnb'))
async def cmd_search_edition_isnb(message: Message, state: FSMContext):
    logger.info('Command search_edition_isnb')
    await message.answer('''Enter isnb to search the edition of book:''')
    await state.set_state(Form.search_edition_isnb)

@search_edition_isnb_router.message(Form.search_edition_isnb)
async def send_info_book_isnb(message: Message, state: FSMContext):
    await state.update_data(search_edition_isnb=message.text)
    user_data = await state.get_data()
    edition_json = fantlab.get_info_about_edition_from_isnb(user_data['search_edition_isnb'])[0]
    edition = Edition(**edition_json)

    await message.answer(
        text=str(edition),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()