from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from handlers.search_states import Form
from aiogram.fsm.context import FSMContext
from db.database import users_db

from create_bot import logger

from bibliosites import fantlab
from db.work_class import Work
from aiogram.types import CallbackQuery

from handlers.common import send_detailed_info, pagination
from keyboards.pagination_kb import create_pagination_keyboard

search_work_name_router = Router()

@search_work_name_router.message(F.text == 'search_work_name')
async def cmd_search_work_name(message: Message, state: FSMContext):
    logger.info('Command search_work_name')
    #await message.answer('''Enter work name:''')
    await message.answer('''Введите название книги:''')
    await state.set_state(Form.search_work_name)


@search_work_name_router.message(Form.search_work_name)
async def send_info_book_isnb(message: Message, state: FSMContext):
    await state.update_data(search_work_name=message.text)
    user_data = await state.get_data()
    users_db[message.from_user.id]['page'] = 1
    #Work = send_info(user_data['search_work_name'], fantlab.get_info_about_Work_from_name, Work)
    book = pagination(user_data['search_work_name'], Work)
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
    #    text=str(Works),
    #    reply_markup=ReplyKeyboardRemove()
    #)
    #await state.clear()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@search_work_name_router.callback_query(F.data == 'backward',Form.search_work_name)
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    logger.info('Click backward')
    user_data = await state.get_data()
    book = pagination(user_data['search_work_name'], Work)
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
@search_work_name_router.callback_query(F.data == 'forward',Form.search_work_name)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    logger.info('Click forward')
    user_data = await state.get_data()
    book = pagination(user_data['search_work_name'], Work)
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
@search_work_name_router.callback_query(F.data == 'download', Form.search_work_name)
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    logger.info('Click download')
    user_data = await state.get_data()
    text = send_detailed_info(user_data['search_work_name'], Work, users_db[callback.from_user.id]['page'])
    #text = book[users_db[callback.from_user.id]['page']]
    await callback.message.answer(text)
    await state.clear()
    logger.info('Stop search_work_name state')