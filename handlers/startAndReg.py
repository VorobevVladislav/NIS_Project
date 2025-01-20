from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram import Router

import aiosqlite

from classes import RegistrationState
import keyboards as kb


startAndReg = Router()


@startAndReg.message(CommandStart(), State(None))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверяем наличие пользователя в базе данных
    # result = await checkRegistration(user_id)

    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT * FROM users WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
    if not result:
        await message.answer(
            f"Привет! Кажется, вы новый пользователь. Хотите зарегистрироваться?",
            reply_markup=kb.registration,
        )
        await state.set_state(RegistrationState.waiting_for_confirmation)
    else:
        # Если пользователь уже зарегистрирован, просто приветствуем его
        await message.answer(
            f"Привет, {username}! Рад вас видеть снова!", reply_markup=kb.menu
        )
        await state.set_state(RegistrationState.confirmated)


@startAndReg.callback_query(F.data == "yes")
async def registrationYes(callback: CallbackQuery, state: FSMContext):
    try:
        # Добавляем нового пользователя в базу данных
        async with aiosqlite.connect("users.db") as db:
            await db.execute(
                "INSERT INTO users (user_id, username, subscribed) VALUES (?, ?, TRUE)",
                (
                    callback.from_user.id,
                    callback.from_user.username,
                ),
            )
            await db.commit()
        await callback.message.answer(
            f"Привет, {callback.from_user.username}! Вы успешно зарегистрированы!",
            reply_markup=kb.menu,
        )
        await state.set_state(RegistrationState.confirmated)
    except Exception as e:
        print(f"Ошибка при обработке регистрации: {e}")
        await callback.message.answer(
            "Произошла ошибка при регистрации. Попробуйте позже."
        )


@startAndReg.callback_query(F.data == "no")
async def registrationNo(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.answer("Регистрация отменена.")
        await state.set_state(RegistrationState.confirmated)
    except Exception as e:
        print(f"Ошибка при обработке регистрации: {e}")
        await callback.message.answer(
            "Произошла ошибка при регистрации. Попробуйте позже."
        )
