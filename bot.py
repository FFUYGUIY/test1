import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

TOKEN = "8952968946:AAHOld9cVCfVOX_y_JAZWncEXNgVfI6Ib4E"


reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Python"), KeyboardButton(text="Java"), KeyboardButton(text="JavaScript")],
    ],
    resize_keyboard=True,
)


inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Документация Python", url="https://docs.python.org/3/")],
        [InlineKeyboardButton(text="Документация JS", url="https://developer.mozilla.org/ru/docs/Web/JavaScript")],
        [InlineKeyboardButton(text="Документация Java", url="https://docs.oracle.com/en/java/"),],
    ]
)



async def cmd_start(message: types.Message):
  await message.answer(
      "Привет! Выберите язык программирования с помощью кнопок ниже:",
      reply_markup=reply_kb,
  )



async def cmd_docs(message: types.Message):
  await message.answer(
      "Выбери язык, чтобы перейти к официальной документации:",
      reply_markup=inline_kb,
  )



async def process_python(message: types.Message):
  await message.answer(
      "Python — это высокоуровневый язык программирования общего назначения, "
      "универсальный, с простым и понятным синтаксисом."
  )


async def process_java(message: types.Message):
  await message.answer(
      "Java — строго типизированный объектно-ориентированный язык программирования, "
      "широко применяемый для разработки корпоративных приложений и Android."
  )


async def process_js(message: types.Message):
  await message.answer(
      "JavaScript — язык программирования, который позволяет реализовать сложную "
      "логику на веб-страницах, делая их интерактивными."
  )


async def main():
  bot = Bot(token=TOKEN)
  dp = Dispatcher(storage=MemoryStorage())


  dp.message.register(cmd_start, Command(commands=["start"]))
  dp.message.register(cmd_docs, Command(commands=["docs"]))

  dp.message.register(process_python, F.text == "Python")
  dp.message.register(process_java, F.text == "Java")
  dp.message.register(process_js, F.text == "JavaScript")

  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())