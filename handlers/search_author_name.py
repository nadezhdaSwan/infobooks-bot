from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from handlers.search_states import Form
from aiogram.fsm.context import FSMContext
from db.database import users_db

from create_bot import logger

from bibliosites import fantlab
from db.author_class import Author

from handlers.common import send_info, pagination
from keyboards.pagination_kb import create_pagination_keyboard

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
    users_db[message.from_user.id]['page'] = 1
    #author = send_info(user_data['search_author_name'], fantlab.get_info_about_author_from_name, Author)
    book = pagination(user_data['search_author_name'], Author)
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{users_db[message.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )
    #await message.answer(
    #    text=str(authors),
    #    reply_markup=ReplyKeyboardRemove()
    #)
    #await state.clear()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@search_author_name_router.callback_query(F.data == 'backward',Form.search_author_name)
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    logger.info('Click backward')
    user_data = await state.get_data()
    book = pagination(user_data['search_author_name'], Author)
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@search_author_name_router.callback_query(F.data == 'forward',Form.search_author_name)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    logger.info('Click forward')
    user_data = await state.get_data()
    book = pagination(user_data['search_author_name'], Author)
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                'forward'
            )
        )
    await callback.answer()
