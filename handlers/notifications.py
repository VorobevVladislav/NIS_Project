from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router


from aiogram import F

import aiosqlite

from classes import RegistrationState
import keyboards as kb

notifications = Router()


# Настройка напоминаний
@notifications.message(F.text == "Напоминания", RegistrationState.confirmated)
async def setNotifications(message: Message):
    await message.answer(
        "Хотели бы вы получать ежедневные напоминания?",
        reply_markup=kb.setNotifications,
    )


# Включение напоминаний
@notifications.message(Command("notifications_on"), RegistrationState.confirmated)
async def enable_notifications(message: Message):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "REPLACE INTO users (user_id, username, subscribed) VALUES (?, ?, TRUE)",
            (
                message.from_user.id,
                message.from_user.username,
            ),
        )
        await db.commit()

    await message.answer(
        "Уведомления включены. Теперь вы будете получать напоминание каждый день."
    )


# Включение напоминаний
@notifications.callback_query(F.data == "able", RegistrationState.confirmated)
async def enable_notifications(callback: CallbackQuery):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "REPLACE INTO users (user_id, username, subscribed) VALUES (?, ?, TRUE)",
            (
                callback.message.from_user.id,
                callback.message.from_user.username,
            ),
        )
        await db.commit()

    await callback.message.answer(
        "Уведомления включены. Теперь вы будете получать напоминание каждый день."
    )


# Выключение напоминаний
@notifications.message(Command("notifications_off"), RegistrationState.confirmated)
async def disable_notifications(message: Message):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "REPLACE INTO users (user_id, username, subscribed) VALUES (?, ?, FALSE)",
            (
                message.from_user.id,
                message.from_user.username,
            ),
        )
        await db.commit()

    await message.answer("Уведомления отключены. Вы не будете получать напоминания.")


# Выключение напоминаний
@notifications.callback_query(F.data == "disable", RegistrationState.confirmated)
async def disable_notifications(callback: CallbackQuery):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "REPLACE INTO users (user_id, username, subscribed) VALUES (?, ?, FALSE)",
            (
                callback.message.from_user.id,
                callback.message.from_user.username,
            ),
        )
        await db.commit()

    await callback.message.answer(
        "Уведомления отключены. Вы не будете получать напоминания."
    )
