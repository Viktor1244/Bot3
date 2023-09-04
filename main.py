from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from decouple import config


bot = Bot(config('API_TOKEN'))
dp = Dispatcher(bot)

questions = [
    {"expression": "35 + 20", "answers": ["55", "50", "60", "45"], "correct": "55"},
    {"expression": "5 * 7", "answers": ["35", "30", "40", "25"], "correct": "35"},
    {"expression": "12 / 4", "answers": ["3", "2", "10", "5"], "correct": "3"},
    {"expression": "20 - 5", "answers": ["15", "66", "25", "100"], "correct": "15"},
    {"expression": "8 * 9", "answers": ["72", "80", "64", "56"], "correct": "72"},
    {"expression": "18 / 3", "answers": ["2", "6", "3", "9"], "correct": "6"},
    {"expression": "7 + 3", "answers": ["11", "12", "13", "10"], "correct": "10"},
    {"expression": "15 - 8", "answers": ["7", "6", "8", "9"], "correct": "7"},
    {"expression": "6 * 5", "answers": ["30", "25", "35", "20"], "correct": "30"},
    {"expression": "21 / 7", "answers": ["3", "2", "4", "5"], "correct": "3"},
    {"expression": "16 + 4", "answers": ["20", "18", "22", "15"], "correct": "20"},
    {"expression": "9 - 3", "answers": ["6", "5", "4", "7"], "correct": "6"},
    {"expression": "10 * 2", "answers": ["20", "15", "25", "12"], "correct": "20"},
    {"expression": "27 / 9", "answers": ["3", "2", "4", "6"], "correct": "3"}
]

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(types.KeyboardButton(text="A"), types.KeyboardButton(text="B"))
keyboard.add(types.KeyboardButton(text="C"), types.KeyboardButton(text="D"))

correct_answers = 0
incorrect_answers = 0
current_question_index = 0  # Змінна для відслідковування поточного питання

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global correct_answers, incorrect_answers, current_question_index
    correct_answers = 0
    incorrect_answers = 0
    current_question_index = 0
    current_question = questions[current_question_index]
    answers = "\n".join([f"{chr(65 + i)}. {ans}" for i, ans in enumerate(current_question['answers'])])
    await message.reply(f"Добро пожаловать в игру!\nИгра началась \n{current_question['expression']}\n{answers}", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text.lower() == 'a' or message.text.lower() == 'b' or message.text.lower() == 'c' or message.text.lower() == 'd')
async def process_answer(message: types.Message):
    global correct_answers, incorrect_answers, current_question_index
    selected_answer = message.text.lower()
    current_question = questions[current_question_index]        
    if message.text == "A":
        correct_answers += 1
        await message.reply("Правильно!")
    else:
        incorrect_answers += 1
        await message.reply(f"Неправильно")

    current_question_index += 1

    if incorrect_answers >= 5 or current_question_index >= len(questions):
        await message.reply(f"Ты достиг 5 неправильных ответов. Твоя оцена – {correct_answers}.Спасибо за игру!")
    else:
        current_question = questions[current_question_index]
        answers = "\n".join([f"{chr(65 + i)}. {ans}" for i, ans in enumerate(current_question['answers'])])
        await message.reply(f"Какой ответь в етом примере: {current_question['expression']}?\n\n{answers}", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
