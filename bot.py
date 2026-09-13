import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router

TOKEN = "8952968946:AAHOld9cVCfVOX_y_JAZWncEXNgVfI6Ib4E"


async def main():
      bot = Bot(token=TOKEN)
      dp = Dispatcher(storage=MemoryStorage())
      dp.include_router(router)
      await dp.start_polling(bot)


if __name__ == "__main__":
      logging.basicConfig(level=logging.INFO, stream=sys.stdout)
      asyncio.run(main())