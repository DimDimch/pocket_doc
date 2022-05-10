import engine as engine
import psycopg2
from psycopg2 import Error
import socket
import enum

disease_list = []
whitelist = []
start_kb = None
condition = None
cursor = None

is_query = False


class MsgDataType(enum.IntEnum):
    ERROR = 0
    STRING = 1
    ARRAY_OF_STRING = 2
    NUMBER = 3


class MsgType(enum.IntEnum):
    ERROR = 0
    QUESTION = 1
    ANSWER = 2
    SYSTEM_INFO = 3


class ClientAnswer:
    def __init__(self, user_id: int, socket_num: int, socket_count: int,
                 msg_data_type: MsgDataType, msg_type: MsgType, msg: str):
        self.user_id = user_id
        self.socket_num = socket_num
        self.socket_count = socket_count
        self.msg_data_type = msg_data_type
        self.msg_type = msg_type
        self.msg = msg


class SocketServer:
    max_connections = 1
    port_num = 8080
    self_ip = socket.gethostname()

    SOCKET_TOTAL_SIZE = 1024
    SOCKET_SYSTEM_SIZE = 10

    listen_socket = None

    def __init__(self):
        self.listen_socket = socket.socket()
        print(self.self_ip)

    def connect(self):
        self.listen_socket.bind(('', self.port_num))
        self.listen_socket.listen(self.max_connections)

    def _process_of_response(self, recv: bytes) -> ClientAnswer:
        system_path: bytes = recv[:self.SOCKET_SYSTEM_SIZE]
        # расшифровываем системную часть сокета
        a = [0, 1, 2, 3, 4]
        user_id = int.from_bytes(system_path[0:4], byteorder='little', signed=False)
        socket_num: int = system_path[4]
        socket_count: int = system_path[5]
        msg_data_type: int = system_path[6]
        msg_type: int = system_path[7]
        # дешифруем все сообщение, потом обрезаем системную часть
        msg: str = recv.decode()
        msg = msg[self.SOCKET_SYSTEM_SIZE:]
        return ClientAnswer(user_id, socket_num, socket_count, msg_data_type, msg_type, msg)

    def server_main_loop(self):
        client_socket, address = self.listen_socket.accept()
        while True:
            total_path = client_socket.recv(self.SOCKET_TOTAL_SIZE)
            if len(total_path) != 0:
                client_answer = self._process_of_response(total_path)
                print(client_answer.msg)
            else:
                self.server_main_loop()

    def send_message(self):
        pass


def main_loop():
    global cursor
    connection = None
    try:
        connection = psycopg2.connect(user="bot", password="RTlpDW", host="localhost", port="5432", database="med")
        connection.autocommit = True
        cursor = connection.cursor()

        create_disease_btn()
        create_whitelist()

        # client_socket = start_socket_server()
        # start_polling(client_socket)
        server = SocketServer()
        server.connect()
        server.server_main_loop()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def start_socket_server():
    listen_socket = socket.socket()
    port = 8080
    max_connections = 1
    ip = socket.gethostname()
    print(ip)

    listen_socket.bind(('', port))
    listen_socket.listen(max_connections)

    client_socket, address = listen_socket.accept()
    return client_socket


def start_polling(client_socket):
    global condition
    message = "Здравствуйте!\nЧто беспокоит вашего ребёнка?\n" + str(disease_list)
    client_socket.send(message.encode())
    while True:
        answer = client_socket.recv(1024).decode()
        if answer in disease_list:
            condition = engine.get_page_id(answer, cursor)
            question, q_type = ask("Да")
        elif answer == "Да" or answer == "Нет":
            question, q_type = ask(answer)
        else:
            client_socket.send("Я вас не понимаю".encode())
            continue

        if q_type == "question":
            client_socket.send(question.encode())
        elif q_type == "answer":
            condition = None
            new_answer = f"Возможно, это: {question.lower()}\n" + "Могу ли я еще чем-то помочь?\nЧто вас беспокоит?"
            client_socket.send(new_answer.encode())
        elif q_type == "error":
            condition = None
            client_socket.send("Ошибка".encode())


def create_disease_btn():
    global start_kb, disease_list
    disease_list = engine.get_diseases_list(cursor)
    disease_list.sort()


def create_whitelist():
    global whitelist
    whitelist = engine.get_whitelist(cursor)


def ask(answer):
    global condition
    message, condition, message_type = engine.get_message(condition, answer, cursor)
    return message, message_type


if __name__ == '__main__':
    main_loop()
