from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
yesButton = KeyboardButton('Да')
noButton = KeyboardButton('Нет')
YesNo_kb = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(yesButton,noButton)