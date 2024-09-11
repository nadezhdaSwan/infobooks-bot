from copy import deepcopy

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db.database import users_db, user_dict_template

from keyboards.all_kb import main_kb

from create_bot import logger

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info('Command start')
#    await message.answer('''
#Hi!
#This bot can search information about the books.
#you can:
#/search_edition_isnb - search edition of book by isnb
#/search_work_name - search work by name
#/search_author_name - search author by name
#''', reply_markup=main_kb())
    await message.answer('''
Привет!
Этот бот может искать информацию о книгах на сайте fantlab.ru. 
Выберите способ поиска:
''', reply_markup = main_kb())
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)