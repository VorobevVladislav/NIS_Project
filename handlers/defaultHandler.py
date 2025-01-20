from aiogram import Router
from aiogram.types import Message

defaultHandler = Router()

# реакция на любое действие
@defaultHandler.message(flags={"priority": -100})
async def answerForEverything(messege: Message):
    await messege.answer("...")