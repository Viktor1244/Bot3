from random import randint, choice
from defs import *
from aiogram import Bot, Dispatcher, executor, types
from decouple import config

from utils import *

bot = Bot(config("API_TOKEN"))
dp = Dispatcher(bot)

score = 0
lose = 0
win = 0

@dp.message_handler(commands=["start"])
async def start(message: types.Message) :
    await message. answer("Привет\nНажми или напишы /game и начни играть")

@dp.message_handler(commands=['game'])
async def game(message: types.Message):
    examples = list(gen_unique_examples().items())
    true_example = choice(examples)
    for i, exaple in enumerate(examples):
        if exaple == true_example:
            examples[i] = (exaple[0], 'Подсказка: true')
        else:
            examples[i] = (exaple[0], 'Подсказка: false')
    keyboard = gen_keyboard(examples)
    text = f"Вибери правильный ответ на пример: {true_example[1]}"
    await message.answer(text, reply_markup=keyboard)
    
@dp.callback_query_handler(text_contains="game_" )
async def game(call: types.CallbackQuery) :
    global score, lose, win
    
    answer = call.data.split('_')[1]
    if "false" in answer:
        await call.answer('не правильно')
        score -= 1
        lose += 1
    elif 'true' in answer:
        await call.answer('правильно')
        score += 1
        win += 1
    if lose == 5 :
        await call.message.answer(f"Ты проиграл.Ваш счет: {score}")
        score = 0
        lose = 0
        win = 0
        return
    examples = list(gen_unique_examples().items())
    true_example = choice(examples)
    for i, exaple in enumerate(examples):
        if exaple == true_example:
            examples[i] = (exaple[0], 'Подсказка: true')
        else:
            examples[i] = (exaple[0], 'Подсказка: false')
    keyboard = gen_keyboard(examples)
    text = f"----Baша таблица----\nПравильно: {win}\nHе правильно: {lose},Вибери правильный ответ на пример: {true_example[1]}"
    await call.message.answer(text, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)