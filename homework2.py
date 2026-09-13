
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command


TOKEN = "8952968946:AAHOld9cVCfVOX_y_JAZWncEXNgVfI6Ib4E"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    await message.answer(
        "Я бот, созданный для выполнения домашнего задания ко второму уроку. "
        "Я умею рассказывать о себе, прощаться и повторять за вами!"
    )

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