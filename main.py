import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена в файле .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

users_data = {}


class Registration(StatesGroup):
    name = State()
    age = State()
    confirm = State()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    first_name = message.from_user.first_name or "Хилола"
    await message.answer(f"Привет, {first_name}!")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "Список доступных команд:\n"
        "/start — Начать работу и получить приветствие\n"
        "/help — Показать список доступных команд\n"
        "/register — Запустить процесс регистрации\n"
        "/profile — Просмотреть данные своего профиля"
    )
    await message.answer(help_text)


@dp.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer("Шаг 1: Введите ваше имя:")


@dp.message(Registration.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(Registration.age)
    await message.answer("Шаг 2: Введите ваш возраст:")


@dp.message(Registration.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            "Это не число! Пожалуйста, введите возраст цифрами:"
        )
        return

    age = int(message.text)
    if age <= 0:
        await message.answer(
            "Возраст должен быть больше 0! Пожалуйста, введите корректный возраст:"
        )
        return

    await state.update_data(age=age)
    await state.set_state(Registration.confirm)

    user_data = await state.get_data()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить", callback_data="confirm_reg"
                ),
                InlineKeyboardButton(
                    text="Начать заново", callback_data="restart_reg"
                ),
            ]
        ]
    )

    await message.answer(
        f"Проверьте введённые данные:\n"
        f"Имя — {user_data['name']}\n"
        f"Возраст — {user_data['age']}",
        reply_markup=keyboard,
    )


@dp.callback_query(Registration.confirm, F.data == "confirm_reg")
async def confirm_registration(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    users_data[callback.from_user.id] = user_data

    await callback.message.answer("Регистрация завершена!")
    await state.clear()
    await callback.answer()


@dp.callback_query(Registration.confirm, F.data == "restart_reg")
async def restart_registration(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.name)
    await callback.message.answer("Начнем заново. Шаг 1: Введите ваше имя:")
    await callback.answer()


@dp.message(Command("profile"))
async def cmd_profile(message: Message):
    user_info = users_data.get(message.from_user.id)
    if user_info:
        await message.answer(
            f"Ваши данные:\n"
            f"Имя — {user_info['name']}\n"
            f"Возраст — {user_info['age']}"
        )
    else:
        await message.answer(
            "Вы не зарегистрированы. Напишите /register, чтобы пройти регистрацию."
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())