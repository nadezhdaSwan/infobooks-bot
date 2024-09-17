from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from handlers.search_states import Form
from aiogram.fsm.context import FSMContext
from db.database import users_db

from create_bot import logger

from bibliosites import fantlab
from db.edition_class import Edition

from handlers.common import send_detailed_info, pagination
from keyboards.pagination_kb import create_pagination_keyboard

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
    users_db[message.from_user.id]['page'] = 1
    #Edition = send_info(user_data['search_edition_isnb'], fantlab.get_info_about_Edition_from_name, Edition)
    book = pagination(user_data['search_edition_isnb'], Edition)
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward',
            'download'     
        )
    )

    #await message.answer(
    #    text=str(Editions),
    #    reply_markup=ReplyKeyboardRemove()
    #)
    #await state.clear()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@search_edition_isnb_router.callback_query(F.data == 'backward',Form.search_edition_isnb)
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    logger.info('Click backward')
    user_data = await state.get_data()
    book = pagination(user_data['search_edition_isnb'], Edition)
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward',
                'download'
            )
        )
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@search_edition_isnb_router.callback_query(F.data == 'forward',Form.search_edition_isnb)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    logger.info('Click forward')
    user_data = await state.get_data()
    book = pagination(user_data['search_edition_isnb'], Edition)
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward',
                'download'
            )
        )
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "download"
# выводит подробную информацию об авторе
@search_edition_isnb_router.callback_query(F.data == 'download', Form.search_edition_isnb)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    logger.info('Click download')
    user_data = await state.get_data()
    text = send_detailed_info(user_data['search_edition_isnb'], Edition, users_db[callback.from_user.id]['page'])
    #text = book[users_db[callback.from_user.id]['page']]
    await callback.message.answer(text)
    await state.clear()
    logger.info('Stop search_edition_isnb state')