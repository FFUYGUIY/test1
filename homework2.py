import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8952968946:AAHOld9cVCfVOX_y_JAZWncEXNgVfI6Ib4E"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Registration(StatesGroup):
    name = State()
    age = State()


profiles = {}
temp_profiles = {}


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
    text = message.text.strip() if message.text else ""
    if not text or len(text) < 2 or text.startswith("/"):
        await message.answer("Это не имя, введите правильное!")
        return
    await state.update_data(name=text)
    await message.answer("Шаг 2: Введите ваш возраст:")
    await state.set_state(Registration.age)


@dp.message(Registration.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Это не число! Пожалуйста, введите возраст цифрами:")
        return

    age = int(message.text)
    if age <= 0 or age > 120:
        await message.answer("Введите корректный возраст цифрами:")
        return

    data = await state.get_data()
    name = data.get("name")

    temp_profiles[message.from_user.id] = {"name": name, "age": age}

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подтвердить", callback_data="confirm_reg"),
                InlineKeyboardButton(text="Начать заново", callback_data="restart_reg")
            ]
        ]
    )

    await message.answer(
        f"Проверьте введённые данные: Имя — {name}, Возраст — {age}",
        reply_markup=keyboard
    )
    await state.clear()


@dp.callback_query(F.data == "confirm_reg")
async def confirm_registration(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id in temp_profiles:
        profiles[user_id] = temp_profiles[user_id]
        del temp_profiles[user_id]
        await callback.message.answer("Регистрация прошла успешно!")
    else:
        await callback.message.answer("Данные не найдены. Пройдите регистрацию заново: /register")
    await callback.answer()


@dp.callback_query(F.data == "restart_reg")
async def restart_registration(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id in temp_profiles:
        del temp_profiles[user_id]

    await callback.message.answer("Регистрация начата заново.\nШаг 1: Введите ваше имя:")
    await callback.answer()
    await state.set_state(Registration.name)


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
    await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())