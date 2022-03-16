from aiogram import Bot, Dispatcher, types
from config import TOKEN
from aiogram.utils import executor
from buttons import yesButton, noButton, YesNo_kb
import engine as engine
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import psycopg2
from psycopg2 import Error


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


disease_list = []
start_kb = None
conditions = {}
cursor = None

def main_loop():
    global cursor
    try:
        connection = psycopg2.connect(user="postgres", password="1234", host="localhost", port="5432", database="med")
        cursor = connection.cursor()

        create_disease_btn()

        executor.start_polling(dp)
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def create_disease_btn():
    global start_kb, disease_list
    disease_list = engine.get_diseases_list(cursor)
    start_kb = ReplyKeyboardMarkup([disease_list], resize_keyboard=True, one_time_keyboard=True)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    conditions[message.from_user.id] = None
    await message.reply("Здравствуйте!\nЧто вас беспокоит?", reply_markup=start_kb)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("я могу по соболезновать")


@dp.message_handler(lambda msg: msg.text in disease_list)
async def echo_message(msg: types.Message):
    conditions[msg.from_user.id] = engine.get_page_id(msg.text, cursor)
    msg.text = "Да"
    await ask(msg)

@dp.message_handler(
    lambda msg: (msg.text == noButton.text or msg.text == yesButton.text) and conditions[msg.from_user.id] is not None)
async def ask(msg: types.Message):
    message, condition, message_type = engine.get_message(conditions[msg.from_user.id], msg, cursor)
    conditions[msg.from_user.id] = condition
    if message_type == "question":
        await bot.send_message(text=message, reply_markup=YesNo_kb, chat_id=msg.from_user.id)
    elif message_type == "answer":
        conditions[msg.from_user.id] = None
        await bot.send_message(text=f"Я думаю это\n{message}", chat_id=msg.from_user.id, reply_markup=start_kb)
        await bot.send_message(text="Могу ли я еще чем-то помочь?\nЧто вас беспокоит?", chat_id=msg.from_user.id)
    elif message_type == "error":
        conditions[msg.from_user.id] = None
        await bot.send_message(text="i don't know", chat_id=msg.from_user.id)


if __name__ == '__main__':
    main_loop()


