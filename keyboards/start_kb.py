from aiogram.types import BotCommand, BotCommandScopeDefault
from create_bot import bot

async def set_commands():
    commands = [BotCommand(command='start', description='description')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())