from classes import RegistrationState
from aiogram import Router
from aiogram.types import Message
from aiogram import F


history = Router()


# История запросов
@history.message(
    (F.text == "/request_history") | (F.text == "История"),
    RegistrationState.confirmated,
    flags={"priority": 10},
)
async def request_history(message: Message):
    await message.answer("История")
    pass
