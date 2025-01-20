from functions.allFunctions import send_reminders, start_db
from config import REMINDERS
from initialisation import dp, bot
from handlers.startAndReg import startAndReg
from handlers.searchByKeywords import searchByKeywords
from handlers.searchByName import searchByName
from handlers.notifications import notifications
from handlers.recomendations import recomendations
from handlers.history import history
from handlers.defaultHandler import defaultHandler


import logging
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from langchain_gigachat import GigaChat


# from google.colab import userdata
# userdata.get('TelegramBot') #7933398928:AAFA1b9dxVdcjAnOqgAHbcZqDR_PqFp7e9g
# from google.colab import userdata
# userdata.get('GigaChatKey')


# from google.colab import drive
# drive.mount('/content/drive')

# # Включаем логирование
# logging.basicConfig(
#     level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__)


async def main():
    dp.include_router(startAndReg)
    dp.include_router(searchByKeywords)
    dp.include_router(searchByName)
    dp.include_router(notifications)
    # dp.include_router(recomendations)
    # dp.include_router(history)
    dp.include_router(defaultHandler)  # В самом конце, чтобы хендлилось последним

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        send_reminders, "cron", hour=REMINDERS[0]["hour"], minute=REMINDERS[0]["minute"]
    )
    scheduler.add_job(
        send_reminders, "cron", hour=REMINDERS[1]["hour"], minute=REMINDERS[1]["minute"]
    )
    scheduler.start()
    dp.startup.register(start_db)
    try:
        print("Бот запущен...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types()
        )  # Запуск бота в режиме опроса
    finally:
        await bot.session.close()
        print("Бот остановлен")


# # Запуск основной функции
# loop = asyncio.get_event_loop()
# task = loop.create_task(main())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
