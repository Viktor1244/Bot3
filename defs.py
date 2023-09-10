import random
from aiogram import *


MATH_OPERATORS = ['+', '-', '*', '/']

def gen_example(min_max_num=(1,10), operators=MATH_OPERATORS) :
    num1 = random.randint (*min_max_num)
    num2 = random.randint (*min_max_num)
    operator = random.choice(MATH_OPERATORS)
    example = f"{num1} {operator} {num2}"
    if operator == '/':
        while num1 % num2 != 0:
            num1 = random.randint(*min_max_num)
            num2 = random.randint(*min_max_num)
            example = f"{num1} {operator} {num2}"
    return example, int(eval(example))

def gen_unique_examples(count=4):
    examples = {}
    while len(examples) != count:
        example, answer = gen_example()
        if answer not in examples:
            examples[answer] = example
    return examples


def gen_keyboard(examples):
    keyboard = types.InlineKeyboardMarkup()
    for value in examples:
        keyboard.add(types.InlineKeyboardButton(text=str(value), callback_data=f"game_{value}"))
    return keyboard





