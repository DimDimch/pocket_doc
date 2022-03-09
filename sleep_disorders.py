# from aiogram import Bot, Dispatcher, types
# from config import TOKEN
# from aiogram.utils import executor
# from buttons import yesButton, noButton, YesNo_kb
# from main import dp

disease = 'Нарушения сна'
question = """Просыпается ли ваш ребенок ночью?"""
questionY = """Имеются ли у ребенка какие-нибудь признаки заболевания: беспричинный плач, повышенная температура или насморк?"""
questionN = """Спит ли ваш ребёнок днём час или около того?"""
questionYN = """Имеются ли у ребенка какие-либо причины для тревоги: домашние неприятности, отсутствие одного из родителей или новая школа?"""
questionYNN = """Ваш ребенок выглядит Да испуганным при пробуждении?"""
questionYNNN = """Просыпается ли ваш ребенок  ночью несколько раз, чтобы помочиться?"""
questionNN = """ваш ребенок обычно плачет, Да когда вы вечером выходите из комнаты?"""
answerYY = """Другое заболевание"""
answerYNY = """Беспокойство"""
answerYNNY = """Кошмарные сновидения"""
answerYNNNY = """инфекции мочевыводящих путей."""
answerNY = """Слишком длительный сон днем"""
answerNNY = """Страх оставаться одному"""
answerNNN = """Пробуждение по ночам без видимой причины"""

"""
правила оформления страницы 
condition = состояние диалога, 1=да 0=нет
get question даёт вопрос на данном этапе состояния 
get answer даёт ответ на данном этапе состояния 
(и то и то возращает вершину графа путь до которой заложен в condition где 1 это лево а 0 это право) 
"""
def get_question(condition):
    if condition == [1]:
        return questionY
    if condition == [1, 0]:
        return questionYN
    if condition == [1, 0, 0]:
        return questionYNN
    if condition == [1, 0, 0, 0]:
        return questionYNNN
    if condition == [0] or condition == [1, 0, 0, 0, 0]:
        return questionN
    if condition == [0, 0] or condition == [1, 0, 0, 0, 0, 0]:
        return questionNN
    return False


def get_answer(condition):
    if condition == [1, 1]:
        return answerYY
    if condition == [1, 0, 1]:
        return answerYNY
    if condition == [1, 0, 0, 1]:
        return answerYNNY
    if condition == [1, 0, 0, 0, 1]:
        return answerYNNNY
    if condition == [0, 1] or condition == [1, 0, 0, 0, 0, 1]:
        return answerNY
    if condition == [0, 0, 1] or condition == [1, 0, 0, 0, 0, 0, 1]:
        return answerNNY
    if condition == [0, 0, 0] or condition == [1, 0, 0, 0, 0, 0, 0]:
        return answerNNN
    return False
# def sleep_disorers_tree(message):
#     await message.reply(question,reply_markup=YesNo_kb)
#     @dp.message_handler(lambda message: message.text == "Да")
#     async def with_puree(message: types.Message):
#         await message.reply(questionY ,reply_markup=YesNo_kb)
