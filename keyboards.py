

def get_custom_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Выбрать", callback_data="btn_select"),
            InlineKeyboardButton(text="Вернуться", callback_data="btn_back")
        ],
        [
            InlineKeyboardButton(text="Удалить", callback_data="btn_delete"),
            InlineKeyboardButton(text="Восстановить", callback_data="btn_restore")
        ]
    ])
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_quiz_keyboard(options):
  buttons = [InlineKeyboardButton(text=opt, callback_data=f"ans_{opt}") for opt in options]
  return InlineKeyboardMarkup(inline_keyboard=[[btn] for btn in buttons])


def get_restart_keyboard():
  return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔄 Сыграть снова", callback_data="restart_quiz")]])