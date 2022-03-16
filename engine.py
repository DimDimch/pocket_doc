from aiogram import types
from buttons import yesButton, noButton


def get_page_id(text, cursor):
    cursor.execute(f"SELECT mt.id FROM main_tree AS mt WHERE mt.text = '{text}';")
    return cursor.fetchone()[0]


def get_diseases_list(cursor) -> []:
    cursor.execute("SELECT mt.text FROM main_tree AS mt WHERE mt.left = mt.right;")
    return [x[0] for x in cursor.fetchall()]


def interpreter_user_answer(msg: types.Message) -> str:
    if msg.text == "Да" or msg.text == yesButton.text or msg.text == "да":
        return "right"
    elif msg.text == "Нет" or msg.text == noButton.text or msg.text == "нет":
        return "left"


def get_message(condition, user_answer, cursor) -> (str, int, str):
    cursor.execute(
        "SELECT main_tree." + str(interpreter_user_answer(user_answer)) + f" FROM main_tree WHERE id = {condition};")
    child_id = cursor.fetchone()[0]
    cursor.execute(f"SELECT mt.text, mt.left, mt.right FROM main_tree AS mt WHERE id = {child_id};")
    message, left_child, right_child = cursor.fetchone()

    print(message, )
    if left_child is None and right_child is None:
        return str(message), child_id, "answer"

    return str(message), child_id, "question"
