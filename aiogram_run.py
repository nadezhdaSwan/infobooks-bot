import asyncio
from create_bot import bot, dp#, scheduler
from handlers.start import start_router
from handlers.search_edition_isnb import search_edition_isnb_router
from handlers.search_work_name import search_work_name_router
from handlers.search_author_name import search_author_name_router
# from work_time.time_func import send_time_msg

from keyboards.start_kb import set_commands

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    dp.include_router(search_edition_isnb_router)
    dp.include_router(search_work_name_router)
    dp.include_router(search_author_name_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())