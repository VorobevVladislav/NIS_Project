from classes import RegistrationState
from aiogram import Router
from aiogram.types import Message
from aiogram import F


recomendations = Router()


# Рекомендации
@recomendations.message(
    (F.text == "/recomendations") | (F.text == "Рекомендации"),
    RegistrationState.confirmated,
    flags={"priority": 10},
)
async def request_history(message: Message):
    await message.answer("Рекомендации")

    pass
