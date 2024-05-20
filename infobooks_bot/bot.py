import os, sys

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config_reader import config

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('''
Hi!
This is bot for searching information about the books.
You can:
/find_book - find book by name + author name
/find_book_isnb - find book from isnb
''')

@dp.message(Command("find_book"))
async def cmd_find_book(message: types.Message):
    await message.answer('On work')

@dp.message(Command("find_book_isnb"))
async def cmd_find_book_isnb(message: types.Message):
    await message.answer('On work')

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())