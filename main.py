from aiogram import Bot, Dispatcher, types
from config import TOKEN
from aiogram.utils import executor
from buttons import *
import engine as engine
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import psycopg2
from psycopg2 import Error

from dermatology.skin_disease.skin_disease import dermatology_make_prediction

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


disease_list = []
whitelist = []
start_kb = None
conditions = {}
cursor = None

is_query = False


def main_loop():
    global cursor
    connection = None
    try:
        connection = psycopg2.connect(user="bot", password="RTlpDW", host="localhost", port="5432", database="med")
        connection.autocommit = True
        cursor = connection.cursor()

        create_disease_btn()
        create_whitelist()

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
    disease_list.sort()
    # disease_list = ("Высокая температура", "Головная боль", "Нарушения сна", "Насморк", "Боль в горле")
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for d in disease_list:
        start_kb.add(d)


def create_whitelist():
    global whitelist
    whitelist = engine.get_whitelist(cursor)
    print(whitelist)


@dp.message_handler(commands=['whitelist'])
async def process_help_command(message: types.Message):
    if message.from_user.id in whitelist:
        await message.reply("Вы уже находитесь в белом списке")
    elif message.text[len("/whitelist "):] == "5qtr4n":
        engine.add_to_whitelist(cursor, int(message.from_user.id))
        whitelist.append(int(message.from_user.id))
        print(whitelist)
        await message.reply("Вы успешно добавлены в белый лист")
    else:
        await message.reply("Неверный пароль")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global whitelist
    if message.from_user.id in whitelist:
        conditions[message.from_user.id] = None
        await message.reply("Здравствуйте!\nЧто беспокоит вашего ребёнка?", reply_markup=start_kb)
    else:
        await message.reply("Недостаточно прав для выполнения данной команды")


@dp.message_handler(commands=['q'])
async def process_help_command(message: types.Message):
    global whitelist
    if message.from_user.id in whitelist:
        await message.reply(engine.run_sql(message.text[3:] + ";", cursor))
    else:
        await message.reply("Недостаточно прав для выполнения данной команды")


@dp.message_handler(commands=['p'])
async def process_help_command(message: types.Message):
    global whitelist
    if message.from_user.id in whitelist:
        await message.reply(engine.return_parents(message.text[3:], cursor))
    else:
        await message.reply("Недостаточно прав для выполнения данной команды")


@dp.message_handler(commands=['diagnoses'])
async def process_help_command(message: types.Message):
    global whitelist
    if message.from_user.id in whitelist:
        await message.reply(engine.get_diagnoses(cursor))
    else:
        await message.reply("Недостаточно прав для выполнения данной команды")


@dp.message_handler(content_types=["photo"])
async def get_photo(message: types.Message):
    global whitelist
    if message.from_user.id in whitelist:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        new_file_path = "dermatology/skin_disease/" + str(message.from_user.id) + ".jpg"
        await bot.download_file(file.file_path, new_file_path)
        await bot.send_message(text='Файл получил, пожалуйста, подождите...', chat_id=message.from_user.id)
        disease = dermatology_make_prediction(str(message.from_user.id) + ".jpg")
        await bot.send_message(text=disease, chat_id=message.from_user.id, reply_markup=start_kb)
    else:
        await message.reply("Недостаточно прав для выполнения данной команды")


@dp.message_handler(lambda msg: msg.text == consulButton.text)
async def consult_doctor(msg: types.Message):
    message = engine.get_doctor_info(cursor, conditions[msg.from_user.id])
    await bot.send_message(text="Вам отлично подойдет:", chat_id=msg.from_user.id, reply_markup=final_kb)
    await bot.send_message(text=message, chat_id=msg.from_user.id, reply_markup=final_kb)


@dp.message_handler(lambda msg: msg.text == againButton.text)
async def start_again(msg: types.Message):
    await process_start_command(msg)


@dp.message_handler(
    lambda msg:
    msg.text in disease_list and
    msg.from_user.id in whitelist
)
async def echo_message(msg: types.Message):
    conditions[msg.from_user.id] = engine.get_page_id(msg.text, cursor)
    msg.text = "Да"
    await ask(msg)


@dp.message_handler(
    lambda msg:
    (msg.text == noButton.text or msg.text == yesButton.text) and
    conditions[msg.from_user.id] is not None and
    msg.from_user.id in whitelist
)
async def ask(msg: types.Message):
    message, condition, message_type = engine.get_message(conditions[msg.from_user.id], msg.text, cursor)
    conditions[msg.from_user.id] = condition
    if message_type == "question":
        await bot.send_message(text=message, reply_markup=YesNo_kb, chat_id=msg.from_user.id)
    elif message_type == "answer":
        # conditions[msg.from_user.id] = None
        await bot.send_message(text=f"Возможно, это: {message.lower()}", chat_id=msg.from_user.id, reply_markup=final_kb)
        descr = engine.get_description(cursor, conditions[msg.from_user.id])
        await bot.send_message(text=descr, chat_id=msg.from_user.id, reply_markup=final_kb)
        spec = engine.get_specialization(cursor, conditions[msg.from_user.id])
        await bot.send_message(text=f"Обратитесь к врачу специализации: {spec.lower()}", chat_id=msg.from_user.id, reply_markup=final_kb)
    elif message_type == "error":
        conditions[msg.from_user.id] = None
        await bot.send_message(text=message, chat_id=msg.from_user.id)


if __name__ == '__main__':
    main_loop()


