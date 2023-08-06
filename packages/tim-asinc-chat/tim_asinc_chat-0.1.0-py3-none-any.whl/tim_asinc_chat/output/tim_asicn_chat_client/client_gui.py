from multiprocessing import Process, JoinableQueue
from socket import *
import json
import time
from metaclass import PortChecker, ClassVerifier
import argparse
import logging
import sys
from PySide6.QtCore import SignalInstance, Signal, QObject
import re
from functools import wraps

PATTERN = r"\{.*?\}\B"


class Client(QObject):
    port = PortChecker()
    text = str()
    hashed_password = None

    def __init__(
        self,
        client_name="username",
        ip_addr="localhost",
        port=7777,
    ):
        QObject.__init__(self)

        self.queue_send = JoinableQueue()
        self.queue_read = JoinableQueue()
        self.new_message = Signal(dict)
        # if ip_addr != "localhost":
        self.ip_addr = ip_addr
        # else:
        #     self.ip_addr = self.parsed_args.addr
        # if port != 7777:
        self.port = port
        # else:
        #     self.port = self.parsed_args.port
        # if client_name != "username":
        self.client_name = client_name
        # else:
        #     self.client_name = self.parsed_args.name
        self.log = logging.getLogger("server")
        self.log.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler(stream=sys.stdout)
        self.log.addHandler(self.handler)

    # @staticmethod
    # def parser():
    #     """
    #     Метод - парсер аргументов коммандной строки
    #     """
    #     parser = argparse.ArgumentParser(description="Server message app")
    #     parser.add_argument(
    #         "--port", metavar="--p", type=int, help="server TCP-port", default=7777
    #     )
    #     parser.add_argument(
    #         "--addr",
    #         metavar="--a",
    #         type=str,
    #         help="server address",
    #         default="localhost",
    #     )
    #     parser.add_argument(
    #         "--name", metavar="--n", type=str, help="client name", default="username"
    #     )
    #     return parser.parse_args()

    def make_connection(self):
        """
        Метод для создания подключения к серверу
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.ip_addr, self.port))
        self.log.info(f"starting whith addres {self.ip_addr} port {self.port}")

    @property
    def close_connection(self):
        """
        Метод для завершения работы клюентского приложения, закрывает 
        запущенные процессы, сокет, и осуществляет выход из приложения
         с кодом 1.
        """
        self.cli_r.kill()
        self.cli_s.kill()
        self.socket.close()
        self.log.info("Bye-bye, darling!")
        exit(0)

    @staticmethod
    def client_send_m(socket, q: JoinableQueue):
        """
        Метод для отправки сообщений на сервер.
        Args:
            socket : экземпляр сокета, который будет отправлять сообщения
            q (JoinableQueue): Очередь, из которой будут извлекаться сообщения
        """
        while True:
            msg = q.get()
            if isinstance(msg, dict):
                socket.send(json.dumps(msg).encode("utf-8"))
            else:
                split_msg = re.findall(PATTERN, msg)
                for el in split_msg:
                    socket.send(json.dumps(el).encode("utf-8"))
            q.task_done()

    @staticmethod
    def client_read(socket, q: JoinableQueue):
        """
        Метод принимает сообщения от сервера.
        Args:
            socket : экземпляр сокета, который будет принимать сообщения
            q (JoinableQueue): очередь, в которую будут помещаться сообщения
        """
        while True:
            data = socket.recv(1024).decode("utf-8")
            if data:
                msg = json.loads(data)
                q.put(msg)

    @property
    def start_message(self):
        """
        Метод, который запускает процессы приема и отправки сообщений
        """
        self.cli_s = Process(
            target=self.client_send_m,
            args=(
                self.socket,
                self.queue_send,
            ),
        )
        self.cli_r = Process(
            target=self.client_read,
            args=(
                self.socket,
                self.queue_read,
            ),
        )
        self.cli_s.start()
        self.cli_r.start()
        self.log.info("Lets start chat!")

    @property
    def client_online_list(self):
        """
        Метод, который запращивает у сервера список клиентов онланй
        """
        self.queue_send.put(
            {
                "action": "get_contacts",
                "name": self.client_name,
                "time": time.time(),
                "destination": "self",
            }
        )

    def client_to_del(self, name: str):
        """
        Метод для удаления клиента из списка контактов

        Args:
            name (str): логин удаляемого клиента
        """
        self.queue_send.put(
            {
                "name": self.client_name,
                "action": "del_contact",
                "contact_to_del": name,
                "time": time.time(),
                "destination": "self",
            }
        )

    def client_to_add(self, name: str):
        """
        Метод для добавления пользователя в список контактов
        Args:
            name (str): login пользователя
        """
        self.queue_send.put(
            {
                "name": self.client_name,
                "action": "add_contact",
                "contact_to_add": name,
                "time": time.time(),
                "destination": "self",
            }
        )

    def register(self, login: str, password: str):
        """
        Метод для регистрации нового пользователя
        Args:
            login (str): логин нового пользователя
            password (str): стока хешированного пароля нового пользователя
        """
        self.queue_send.put(
            {
                "action": "register",
                "name": login,
                "password": password,
                "time": time.time(),
                "destination": "self",
            }
        )

    @property
    def presense(self):
        """
        Сервисное сообщение о подключении пользователя
        """
        self.queue_send.put(
            {
                "name": self.client_name,
                "hashed_password": self.hashed_password,
                "action": "presense",
                "time": time.time(),
                "destination": "self",
            }
        )

    def auth(self, msg: str):
        """
        Метод для авторизации пользователя на сервере

        Args:
            msg (str): Случайно-сгенерированная на сервере строка
        """
        self.queue_send.put(
            {
                "login": self.client_name,
                "hashed_password": self.hashed_password,
                "b_stryng": msg,
                "action": "auth",
                "time": time.time(),
                "destination": "self",
            }
        )

    def send_message(self, text: str, destination="self"):
        """
        Метод для отправки сообщения на сервер

        Args:
            text (str): текст отправляемого сообщения
            destination (str, optional): получатель сообщения. Defaults to "self".
        """
        self.text = text
        if self.text.startswith("#e"):
            self.close_connection
        elif self.text.startswith("#cli"):
            self.queue_send.put(
                {
                    "name": self.client_name,
                    "msg": "",
                    "action": "get_contacts",
                    "time": time.time(),
                }
            )
        elif self.text.startswith("#h"):
            print(
                "Chat command: \n",
                "#e - exit\n",
                "#h - help\n",
                "#cli - online clients list\n",
                "#add:[frend_name] - add frend to contact",
                "#del:[frend_name] - delete frend from contact",
                "#fr - get frend list",
            )
        elif self.text.startswith("#add"):
            frend_name = self.text.split("#add:")
            self.queue_send.put(
                {
                    "name": self.client_name,
                    "msg": "",
                    "action": "add_contact",
                    "contact_to_add": frend_name[1],
                    "time": time.time(),
                    "destination": "self",
                }
            )
        elif self.text.startswith("#del"):
            frend_name = self.text.split("#del:")
            self.queue_send.put(
                {
                    "name": self.client_name,
                    "msg": "",
                    "action": "del_contact",
                    "contact_to_del": frend_name[1],
                    "time": time.time(),
                    "destination": "self",
                }
            )
        elif self.text.startswith("#fr"):
            self.queue_send.put(
                {
                    "name": self.client_name,
                    "msg": "",
                    "action": "get_frend_list",
                    "time": time.time(),
                    "destination": "self",
                }
            )
        else:
            self.queue_send.put(
                {
                    "name": self.client_name,
                    "msg": self.text,
                    "action": "msg",
                    "time": time.time(),
                    "destination": destination,
                }
            )
        self.text = None

    @property
    def start_chat(self):
        """
        Метод для запуска клиентской части приложения
        """
        self.make_connection()
        self.start_message


if __name__ == "__main__":
    Client().start_chat
