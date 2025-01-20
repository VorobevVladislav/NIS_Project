from config import LISA_TOKEN, GIGACHATKEY, TOKEN


from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from langchain_gigachat import GigaChat
from aiogram import Router


token = LISA_TOKEN
GigaChatKey = GIGACHATKEY

# Инициализация бота и диспетчера
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


llm = GigaChat(credentials=GigaChatKey, model="GigaChat:latest", verify_ssl_certs=False)

