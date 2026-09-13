
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Токен, который вы нашли
TOKEN = "8952968946:AAHOld9cVCfVOX_y_JAZWncEXNgVfI6Ib4E"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Registration(StatesGroup):
    name = State()
    age = State()


profiles = {}


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Бот успешно работает.")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Список доступных команд:\n"
        "/start — Запустить бота\n"
        "/help — Показать список команд\n"
        "/register — Зарегистрироваться\n"
        "/profile — Посмотреть свой профиль\n"
        "/about — Узнать о боте"
    )


@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    await message.answer(
        "Я бот, созданный для выполнения домашнего задания. Я могу повторять за вами, "
        "прощаться по слову 'пока', регистрировать вас и показывать ваш профиль."
    )


@dp.message(Command("register"))
async def cmd_register(message: types.Message, state: FSMContext):
    await message.answer("Шаг 1: Введите ваше имя:")
    await state.set_state(Registration.name)


@dp.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Шаг 2: Введите ваш возраст:")
    await state.set_state(Registration.age)


@dp.message(Registration.age)
async def process_age(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    age = message.text

    profiles[message.from_user.id] = {"name": name, "age": age}

    await message.answer(f"Проверьте введённые данные: Имя — {name}, Возраст — {age}")
    await message.answer("Регистрация завершена!")
    await state.clear()


@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    user_data = profiles.get(message.from_user.id)
    if user_data:
        await message.answer(f"Ваши данные: Имя — {user_data['name']}, Возраст — {user_data['age']}")
    else:
        await message.answer("У вас нет профиля. Введите /register, чтобы зарегистрироваться.")


@dp.message(F.text.lower() == 'пока')
async def send_goodbye(message: types.Message):
    await message.answer("До скорой встречи!")


@dp.message()
async def echo(message: types.Message):
    await message.send_copy(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

