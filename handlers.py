from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import get_quiz_keyboard, get_restart_keyboard

router = Router()

QUESTIONS = [
    {
        "question": "1. Какой язык программирования является основным для разработки под Android?",
        "options": ["Python", "Java", "C++"],
        "answer": "Java",
    },
    {
        "question": "2. Что означает аббревиатура HTML?",
        "options": [
            "HyperText Markup Language",
            "High Tech Modern Language",
            "Hyper Transfer Machine Language",
        ],
        "answer": "HyperText Markup Language",
    },
    {
        "question": "3. Какой оператор используется для создания функции в Python?",
        "options": ["func", "def", "lambda"],
        "answer": "def",
    },
    {
        "question": "4. Какая база данных является реляционной?",
        "options": ["MongoDB", "PostgreSQL", "Redis"],
        "answer": "PostgreSQL",
    },
    {
        "question": "5. Что возвращает выражение 3 == 3 в Python?",
        "options": ["True", "False", "None"],
        "answer": "True",
    },
    {
        "question": "6. Какой тег используется для переноса строки в HTML?",
        "options": ["<br>", "<p>", "<hr>"],
        "answer": "<br>",
    },
    {
        "question": "7. Что такое Git?",
        "options": [
            "Язык программирования",
            "Система контроля версий",
            "Текстовый редактор",
        ],
        "answer": "Система контроля версий",
    },
    {
        "question": "8. Какой метод используется для добавления элемента в конец списка Python?",
        "options": ["add()", "push()", "append()"],
        "answer": "append()",
    },
]


class QuizState(StatesGroup):
  question_index = State()
  score = State()


@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
  await state.clear()
  await message.answer("Привет! Добро пожаловать на викторину.\nНажми /quiz, чтобы начать игру!")


@router.message(F.text == "/quiz")
async def start_quiz(message: types.Message, state: FSMContext):
  await state.set_state(QuizState.question_index)
  await state.update_data(question_index=0, score=0)
  await send_question(message, state)


async def send_question(message_or_callback, state: FSMContext):
  data = await state.get_data()
  index = data.get("question_index", 0)

  if index < len(QUESTIONS):
    q_data = QUESTIONS[index]
    kb = get_quiz_keyboard(q_data["options"])
    text = f"Вопрос {index + 1} из {len(QUESTIONS)}:\n\n{q_data['question']}"

    if isinstance(message_or_callback, types.CallbackQuery):
      await message_or_callback.message.edit_text(text, reply_markup=kb)
    else:
      await message_or_callback.answer(text, reply_markup=kb)
  else:
    score = data.get("score", 0)
    text = f"Викторина завершена! 🎉\nВаш результат: {score} из {len(QUESTIONS)}"
    kb = get_restart_keyboard()

    if isinstance(message_or_callback, types.CallbackQuery):
      await message_or_callback.message.edit_text(text, reply_markup=kb)
    else:
      await message_or_callback.answer(text, reply_markup=kb)

    await state.clear()


@router.callback_query(F.data.startswith("ans_"))
async def check_answer(callback: types.CallbackQuery, state: FSMContext):
  selected_answer = callback.data.split("_", 1)[1]
  data = await state.get_data()
  index = data.get("question_index", 0)
  score = data.get("score", 0)

  correct_answer = QUESTIONS[index]["answer"]

  if correct_answer == selected_answer:
    score += 1
    feedback = "Верно! ✅"
  else:
    feedback = f"Неверно! ❌\nПравильный ответ: {correct_answer}"

  await callback.answer(feedback, show_alert=True)

  await state.update_data(question_index=index + 1, score=score)
  await send_question(callback, state)


@router.callback_query(F.data == "restart_quiz")
async def restart_quiz(callback: types.CallbackQuery, state: FSMContext):
  await state.set_state(QuizState.question_index)
  await state.update_data(question_index=0, score=0)
  await send_question(callback, state)
  await callback.answer()