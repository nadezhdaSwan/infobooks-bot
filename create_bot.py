import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
#from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.cache_manager_redis import CacheManager

#from db_handler.db_class import PostgresHandler

#pg_db = PostgresHandler(config('PG_LINK'))
#scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
#admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
cache = CacheManager()

logging.basicConfig(filename='infobooks_bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=MemoryStorage())