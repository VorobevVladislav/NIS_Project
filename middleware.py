from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
import aiosqlite
from aiogram import types
from aiogram.fsm.context import FSMContext
from classes import *


class Middleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        print("Действия до обработчика")
        check_registration()
        result = await handler(event, data)
        print("Действия после обработчика")
        return result


# Команды бота
# @router.message(CommandStart(), State(None))
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверяем наличие пользователя в базе данных
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT * FROM users WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()

    if not result:
        # Если пользователя нет в базе, предлагаем зарегистрироваться
        await message.answer(
            f"Привет! Кажется, вы новый пользователь. Хотите зарегистрироваться? (Да/Нет)"
        )
        await state.set_state(RegistrationState.waiting_for_confirmation)
    else:
        # Если пользователь уже зарегистрирован, просто приветствуем его
        await message.answer(f"Привет, {username}! Рад вас видеть снова!")
        await state.set_state(RegistrationState.confirmated)


# Обработка ответа на предложение зарегистрироваться
# @router.message(RegistrationState.waiting_for_confirmation)
async def handle_registration_response(message: types.Message, state: FSMContext):
    try:
        if "да" in message.text.lower():
            # Добавляем нового пользователя в базу данных
            async with aiosqlite.connect("users.db") as db:
                await db.execute(
                    "INSERT INTO users (user_id, username, subscribed) VALUES (?, ?, TRUE)",
                    (
                        message.from_user.id,
                        message.from_user.username,
                    ),
                )
                await db.commit()

            await message.answer(
                f"Привет, {message.from_user.username}! Вы успешно зарегистрированы!"
            )
            await state.set_state(RegistrationState.confirmated)
        else:
            await message.answer("Регистрация отменена.")
    except Exception as e:
        print(f"Ошибка при обработке регистрации: {e}")
        await message.answer("Произошла ошибка при регистрации. Попробуйте позже.")


async def check_registration(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверяем наличие пользователя в базе данных
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT * FROM users WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()

    if not result:
        # Если пользователя нет в базе, предлагаем зарегистрироваться
        await message.answer(
            f"Привет! Кажется, вы новый пользователь. Хотите зарегистрироваться? (Да/Нет)"
        )
        await state.set_state(RegistrationState.waiting_for_confirmation)

    try:
        if "да" in message.text.lower():
            # Добавляем нового пользователя в базу данных
            async with aiosqlite.connect("users.db") as db:
                await db.execute(
                    "INSERT INTO users (user_id, username, subscribed) VALUES (?, ?, TRUE)",
                    (
                        message.from_user.id,
                        message.from_user.username,
                    ),
                )
                await db.commit()

            await message.answer(
                f"Привет, {message.from_user.username}! Вы успешно зарегистрированы!"
            )
            await state.set_state(RegistrationState.confirmated)
        else:
            await message.answer("Регистрация отменена.")
    except Exception as e:
        print(f"Ошибка при обработке регистрации: {e}")
        await message.answer("Произошла ошибка при регистрации. Попробуйте позже.")
