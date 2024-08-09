from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from create_bot import logger

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info('Command start')
    await message.answer('''
Hi!
This bot can search information about the books.
You can:
/search_edition_isnb - search edition of book by isnb
/search_work_name - search work by name
/search_author_name - search author by name
''')