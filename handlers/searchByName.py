from classes import RegistrationState
from aiogram import Router
from aiogram.types import Message
from aiogram import F


searchByName = Router()


# Найти статью по названию
@searchByName.message(
    (F.text == "/find_by_name") | (F.text == "Найти статью по названию"),
    RegistrationState.confirmated,
    flags={"priority": 10},
)
async def find_by_name(message: Message):
    await message.answer("по названию")
    pass
