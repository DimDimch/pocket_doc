from aiogram import types
from buttons import yesButton, noButton


def run_sql(sql, cursor):
    result = ""
    try:
        cursor.execute(sql)
        count = 0
        for i in cursor.fetchall():
            result += "- "
            if len(i) == 1:
                result += str(i[0])
            else:
                result += str(i)
            result += "\n"
            count += 1
        result += f"\n {count} rows"
    except Exception as error:
        result = str(error)
    return result


def return_parents(node, cursor) -> str:
    def create_good_view(arr: [[]]):
        def one_branch(branch):
            res = ""
            branch.reverse()
            res += "Страница: " + str(branch[0][0]) + "\n"
            for i in range(1, len(branch) - 1):
                res += "Вопрос: " + str(branch[i][0]) + "\nОтвет: " + str(branch[i][1]) + "\n"
            res += "Диагноз: " + str(branch[-1][0])
            return res

        count_branch = len(arr)
        if count_branch > 1:
            count_branch -= 1

        result = f"Ветвей, ведущих к данному диагнозу: {count_branch}\n"

        for i in range(count_branch):
            result += f"\n\nВетвь {i + 1}:\n\n"
            result += one_branch(arr[i])

        return result

    def find_parents(id_node, node_text, answer) -> [[]]:
        nonlocal cursor
        cursor.execute(f"SELECT mt.id, mt.text, mt.left, mt.right FROM main_tree AS mt WHERE ((mt.left = {id_node}) or (mt.right = {id_node}))")
        parents = cursor.fetchall()
        result = [[(node_text, answer)]]
        check = 0

        for i in range(len(parents)):
            if parents[i][3] == id_node:
                answer = "Да"
            else:
                answer = "Нет"
            temp = find_parents(parents[i][0], parents[i][1], answer)
            if len(parents) > 1:
                result.append(result[i].copy())

            for j in range(len(temp)):
                if len(temp) > 1:
                    result[i].append(temp[j])

                else:
                    for k in range(len(temp[0])):
                        result[i].append(temp[0][k])

        return result

    cursor.execute(f"SELECT mt.id, mt.text FROM main_tree AS mt WHERE mt.text = '{node}'")
    report = cursor.fetchone()
    r = find_parents(report[0], report[1], "Да")

    return create_good_view(r)


def get_page_id(text, cursor):
    cursor.execute(f"SELECT mt.id FROM main_tree AS mt WHERE mt.text = '{text}' ORDER BY mt.text;")
    return cursor.fetchone()[0]


def get_diseases_list(cursor) -> []:
    cursor.execute("SELECT mt.text FROM main_tree AS mt WHERE (mt.left = mt.right) AND mt.left != -1;")
    return [x[0] for x in cursor.fetchall()]


def get_whitelist(cursor) -> []:
    cursor.execute("SELECT bu.id_user FROM bot_users AS bu WHERE bu.role = 'admin';")
    return [int(x[0]) for x in cursor.fetchall()]


def add_to_whitelist(cursor, id_user) -> []:
    cursor.execute(f"INSERT INTO bot_users VALUES('{id_user}', 'admin');")


def get_diagnoses(cursor):
    return run_sql(
        "SELECT mt.text FROM main_tree AS mt WHERE mt.left is null AND mt.right is null",
        cursor
    )


def get_doctor_info(cursor, result_id) -> str:
    cursor.execute(f"SELECT mt.spec FROM main_tree AS mt WHERE mt.id = '{result_id}';")
    spec = cursor.fetchone()[0]
    cursor.execute(f"SELECT doc.name, doc.spec, doc.exp, doc.phone_num, doc.clinic FROM doctors AS doc WHERE doc.spec LIKE '{spec}%';")
    result = ""
    x = cursor.fetchone()
    title = ['ФИО: ', 'Специальность: ', 'Стаж: ', 'Тел.: ', 'Клиника: ']
    for i in range(len(x)):
        if title[i] == 'Стаж: ':
            result += title[i] + str(x[i]) + ' лет' + '\n'
        else:
            result += title[i] + str(x[i]) + '\n'
    return result


def get_description(cursor, result_id) -> str:
    cursor.execute(f"SELECT mt.descr FROM main_tree AS mt WHERE mt.id = '{result_id}';")
    return cursor.fetchone()[0]


def get_specialization(cursor, result_id) -> str:
    cursor.execute(f"SELECT mt.spec FROM main_tree AS mt WHERE mt.id = '{result_id}';")
    return cursor.fetchone()[0]


def interpreter_user_answer(msg: str) -> str:
    if msg == "Да" or msg == yesButton.text or msg == "да":
        return "right"
    elif msg == "Нет" or msg == noButton.text or msg == "нет":
        return "left"


def get_message(condition, user_answer, cursor) -> (str, int, str):
    cursor.execute(
        "SELECT main_tree." + str(interpreter_user_answer(user_answer)) + f" FROM main_tree WHERE id = {condition};")
    child_id = cursor.fetchone()[0]
    cursor.execute(f"SELECT mt.text, mt.left, mt.right FROM main_tree AS mt WHERE id = {child_id};")
    message, left_child, right_child = cursor.fetchone()

    print(message)
    if left_child is None and right_child is None:
        return str(message), child_id, "answer"

    if left_child == right_child:
        if left_child != -1:
            cursor.execute(f"SELECT mt.text, mt.left, mt.right FROM main_tree AS mt WHERE id = {right_child};")
            message, left_child, right_child = cursor.fetchone()
        else:
            return str("Данная ветка еще не прописана, выполните команду /start"), child_id, "error"

    return str(message), child_id, "question"
