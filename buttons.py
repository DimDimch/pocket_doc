from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

yesButton = KeyboardButton('Да')
noButton = KeyboardButton('Нет')
# maybeButton = KeyboardButton('Не знаю')
YesNo_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(yesButton, noButton)

consulButton = KeyboardButton('Посоветовать врача')
# descriptionButton = KeyboardButton('Подробнее о диагнозе')
againButton = KeyboardButton('Начать заново')
final_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(consulButton, againButton)