import numpy as np
import pandas as pd
import asyncio
from aiogram import Bot, Dispatcher, types
from config import TOKEN
from aiogram.utils import executor
from buttons import yesButton, noButton, YesNo_kb
import sleep_disorders as sd
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# button_hi = KeyboardButton('Здрваствуйте доктор')
# greet_kb = ReplyKeyboardMarkup()
# greet_kb.add(button_hi)
# @dp.message_handler()
# async def process_start_command(message: types.Message):
#     await message.reply("Привет!", reply_markup=greet_kb)

disease1 = KeyboardButton(sd.disease)
start_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(disease1)
condition=list()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    condition = list()
    await message.reply("Здравствуйте!\nЧто вас беспокоит?", reply_markup=start_kb)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("я могу по соболезновать")


# @dp.message_handler(lambda message: message.text == disease1)
# def sd_tree(message):
@dp.message_handler(lambda message: message.text == disease1.text and condition==list())
# @dp.message_handler(lambda message: message.text == disease1 and condition==list())
async def echo_message(msg: types.Message):
    condition.append(1)
    await bot.send_message(text=sd.question,chat_id=msg.from_user.id, reply_markup=YesNo_kb)

@dp.message_handler(lambda message: message.text == yesButton.text and condition[0]==1)
async def ask(msg: types.Message):
    condition.append(1)
    question=sd.get_question(condition[1:])
    if question:
        await bot.send_message(text=question, reply_markup=YesNo_kb,chat_id=msg.from_user.id)
    else:
        answer=sd.get_answer(condition[1:])
        if answer:
            await bot.send_message(text=answer,chat_id=msg.from_user.id)
        else:
            await bot.send_message(text="i don't know",chat_id=msg.from_user.id)

@dp.message_handler(lambda message: message.text == noButton.text and condition[0] == 1)
async def ask(msg: types.Message):
    condition.append(0)
    question = sd.get_question(condition[1:])
    if question:
        await bot.send_message(text=sd.question, reply_markup=YesNo_kb,chat_id=msg.from_user.id)
    else:
        answer = sd.get_answer(condition[1:])
        if answer:
            await bot.send_message(text=answer,chat_id=msg.from_user.id)
        else:
            await bot.send_message(text="i don't know",chat_id=msg.from_user.id)
    # @dp.message_handler(lambda message: message.text == "Да")
    # async def with_puree(message: types.Message):
    #     await bot.send_message(sd.questionY, reply_markup=YesNo_kb)
if __name__ == '__main__':
    executor.start_polling(dp)
# if __name__ == '__main__':
#     bot = Bot(token=TOKEN)
#     dp = Dispatcher(bot)
