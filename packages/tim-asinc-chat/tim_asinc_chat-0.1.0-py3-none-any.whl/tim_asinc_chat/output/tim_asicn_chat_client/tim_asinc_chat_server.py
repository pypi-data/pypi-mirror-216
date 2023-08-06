import argparse
import json
import logging
import hmac
import hashlib
import os
import random
import re
import string
import select
import sys
import time
from socket import *
from sqlalchemy.orm import Session
from sqlalchemy import select as SEL
from models import Client, engine, History, Contacts
from metaclass import ClassVerifier, PortChecker


PATTERN = r"\{.*?\}\B"
SICRET_KEY = "my_sickret_key"


class Server(metaclass=ClassVerifier):
    clients = []
    port = PortChecker()
    socket = socket()

    def __init__(self, ip_addr="localhost", port=7777, max_clients=5, timeout=0.2):
        """
        Args:
            ip_addr (str, optional): IP адрес сервера. Defaults to 'localhost'.
            port (int, optional): Порт сервера. Defaults to 7777.
            max_clients (int, optional): Количество клиентов. Defaults to 5.
            timeout (float, optional): Таймаут. Defaults to 0.2.
        """
        self.parsed_args = self.parser()
        if ip_addr != "localhost":
            self.ip_addr = ip_addr
        else:
            self.ip_addr = self.parsed_args.addr
        if port != 7777:
            self.port = port
        else:
            self.port = self.parsed_args.port
        self.max_clients = max_clients
        self.timeout = timeout
        self.log = logging.getLogger("server")
        self.log.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler(stream=sys.stdout)
        self.log.addHandler(self.handler)

    @staticmethod
    def parser():
        """
        Метод - парсер аргументов коммандной строки
        """
        parser = argparse.ArgumentParser(description="Server message app")
        parser.add_argument(
            "--port", metavar="--p", type=int, help="server TCP-port", default=7777
        )
        parser.add_argument(
            "--addr",
            metavar="--a",
            type=str,
            help="server address",
            default="localhost",
        )
        return parser.parse_args()

    def run_server(self):
        """
        Метод создает сокет сервера, и запускает его работу
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.ip_addr, self.port))
        self.log.info(f"starting whith addres {self.ip_addr} port {self.port}")
        self.socket.listen(self.max_clients)
        self.socket.settimeout(self.timeout)

        while True:
            try:
                conn, addr = self.socket.accept()
                self.log.info(f"start connection on address: {addr}")
            except OSError as e:
                pass
            else:
                print(f"Получен запрос на соединение от {str(addr)}")
                self.clients.append(conn)
            finally:
                self.wait = 0.2
                self.r = []
                self.w = []
                try:
                    self.r, self.w, e = select.select(
                        self.clients, self.clients, [], self.wait
                    )
                except:
                    pass
                requests = self.read_requests
                if requests:
                    self.write_response(requests)

    @property
    def read_requests(self):
        """
        Метод для чтения сообщений приходящих на сервер

        Returns:
            dict: возвращает словарь
        """
        response = {}
        for sock in self.r:
            try:
                data = sock.recv(1024).decode("utf-8")
            except:
                with Session(engine) as s:
                    #  при отключении клиента по его адресу и порту находим в БД запись
                    #  очищаем data, убираем статус онлайн
                    find_client = s.scalar(
                        SEL(Client).where(Client.data == str(sock.getpeername()))
                    )
                    find_client.status_online = False
                    find_client.is_authenticated = False
                    find_client.data = None
                    s.commit()
                    print(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
                    sock.close()
                    self.clients.remove(sock)
            else:
                check_sock, check_data = self.data_analisis(sock, data)
                response[check_sock] = check_data

        return response

    def sender(self, msg: dict, sock):
        """
        Метод для отправки сообщений клиентам

        Args:
            msg (dict): сообщение для отправки
            sock ([type]): сокет для отправления
        """
        resp = json.dumps(msg).encode("utf-8")
        try:
            sock.send(resp)
        except:
            with Session(engine) as s:
                #  при отключении клиента по его адресу и порту находим в БД запись
                #  очищаем data, убираем статус онлайн
                find_client = s.scalar(
                    SEL(Client).where(Client.data == str(sock.getpeername()))
                )
                find_client.status_online = False
                find_client.is_authenticated = False
                find_client.data = None
                s.commit()
            print(f"Клиент {sock.fileno()} {sock.getpeername()} отключился")
            sock.close()
            self.clients.remove(sock)

    def write_response(self, requests: dict):
        """
        Метод для поиска сокета адресата сообщения и его отправки

        Args:
            requests (dict): словарь, в котором ключ - сокет, значение  - словарь с сообщением
        """
        for sock_msg in requests:
            if requests[sock_msg]["destination"] == "self":
                self.sender(requests[sock_msg], sock_msg)

            else:
                with Session(engine) as s:
                    # Ищем адресата сообщения:
                    find_user = s.scalar(
                        SEL(Client).where(
                            Client.login == requests[sock_msg]["destination"]
                        )
                    )

                for sock in self.w:
                    if (
                        str(sock.getpeername()) == find_user.data
                        and str(sock.fileno()) == find_user.sock_number
                    ):
                        self.sender(requests[sock_msg], sock)

    def data_analisis(self, sock, data):
        """
        data_analisis - метод - "перехватчик", анализирует сообщения,
        пользовательские пересылает без изменений, системные обрабатывает,
        на выдох отправляет декодированные данные из json
        """
        try:
            ansver = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            print(f"some error:\n{e}\ndata:\n{data}")
            return sock, data
        else:
            if ansver["action"] == "presense":
                user = ansver["name"]

                with Session(engine) as s:
                    _find_login = s.scalar(
                        SEL(Client).where(
                            Client.login.in_(
                                [
                                    user,
                                ]
                            )
                        )
                    )

                    message = "".join(
                        random.SystemRandom().choice(
                            string.ascii_letters + string.digits
                        )
                        for _ in range(25)
                    )

                    hash_msg = hmac.new(
                        SICRET_KEY.encode("utf-8"),
                        message.encode("utf-8"),
                        hashlib.sha256,
                    )
                    digest = hash_msg.hexdigest()
                    _find_login.auth_string = digest
                    _find_login.data = str(sock.getpeername())
                    _find_login.status_online = True
                    _find_login.sock_number = sock.fileno()

                    s.commit()

                response = {
                    "name": "server",
                    "b_string": message,
                    "action": "auth",
                    "time": time.time(),
                    "destination": "self",
                    # 'auth_state': True,
                    "response": 200,
                }
                return sock, response

            if ansver["action"] == "msg":
                user = ansver["name"]
                with Session(engine) as s:
                    _find_login = s.scalar(
                        SEL(Client).where(
                            Client.login.in_(
                                [
                                    user,
                                ]
                            )
                        )
                    )

                    _find_login.status_online = True

                    # Для каждого пакета будем писать историю:
                    _history = History(
                        client_login=ansver["name"],
                        client_ip=sock.getpeername(),
                        # Долой приватность, пишим все к себе в базу!!!
                        client_message=ansver["msg"],
                    )
                    s.add(_history)
                    s.commit()

                return sock, ansver

            elif ansver["action"] == "get_contacts":
                with Session(engine) as s:
                    find_list = s.execute(
                        SEL(Client.login).where(Client.status_online == True)
                    ).all()
                    cli_list = [el[0] for el in find_list]
                    find_list_2 = s.execute(
                        SEL(Contacts.owner_frend).where(
                            Contacts.owner_login == ansver["name"]
                        )
                    ).all()
                    frend_list = [el[0] for el in find_list_2]

                    client = s.scalar(SEL(Client).where(Client.login == ansver["name"]))

                    response = {
                        "name": "server",
                        "cli_online": cli_list,
                        "frends": frend_list,
                        "action": "get_contacts",
                        "auth_state": client.is_authenticated,
                        "time": time.time(),
                        "destination": "self",
                        "response": 200,
                    }
                return sock, response

            elif ansver["action"] == "add_contact":
                with Session(engine) as s:
                    new_frend = Contacts(
                        owner_login=ansver["name"], owner_frend=ansver["contact_to_add"]
                    )
                    s.add(new_frend)
                    s.commit()

                response = {
                    "name": "server",
                    "msg": f'client {ansver["contact_to_add"]} add to contact list',
                    "action": "msg",
                    "time": time.time(),
                    "destination": "self",
                    "response": 201,
                }
                return sock, response

            elif ansver["action"] == "del_contact":
                with Session(engine) as s:
                    del_frend = s.scalar(
                        SEL(Contacts)
                        .where(Contacts.owner_login == ansver["name"])
                        .where(Contacts.owner_frend == ansver["contact_to_del"])
                    )

                    s.delete(del_frend)
                    s.commit()

                response = {
                    "name": "server",
                    "msg": f'client {ansver["contact_to_del"]} del from contact list',
                    "action": "msg",
                    "time": time.time(),
                    "destination": "self",
                    "response": 201,
                }
                return sock, response

            elif ansver["action"] == "get_frend_list":
                with Session(engine) as s:
                    find_list = s.execute(
                        SEL(Contacts.owner_frend).where(
                            Contacts.owner_login == ansver["name"]
                        )
                    ).all()
                    frend_list = [el[0] for el in find_list]
                    response = {
                        "name": "server",
                        "frend_list": frend_list,
                        "action": "get_frend_list",
                        "time": time.time(),
                        "destination": "self",
                        "response": 200,
                    }
                return sock, response

            elif ansver["action"] == "register":
                user = ansver["name"]
                with Session(engine) as s:
                    _find_login = s.scalar(
                        SEL(Client).where(
                            Client.login.in_(
                                [
                                    user,
                                ]
                            )
                        )
                    )

                    # Создаем первичную запись о клиенте, если клиента с таким логином еще не существовало
                    if not _find_login:
                        _client = Client(
                            login=ansver["name"],
                            #  в data храним адрес и порт для идентификации клиента и его соединения
                            password=ansver["password"],
                            is_authenticated=True,
                            data=str(sock.getpeername()),
                            sock_number=sock.fileno(),
                            status_online=True,
                        )
                        # применяем изменения в БД
                        s.add(_client)
                        s.commit()

                        response = {
                            "name": "server",
                            "msg": f'client {ansver["name"]} add to Chat DB',
                            "action": "register_sucsess",
                            "auth_state": _client.is_authenticated,
                            "time": time.time(),
                            "destination": "self",
                            "response": 201,
                        }

                        return sock, response
                    else:
                        response = {
                            "name": "server",
                            "msg": f'client {ansver["name"]} exist',
                            "action": "register_exist",
                            "time": time.time(),
                            "auth_state": _find_login.is_authenticated,
                            "destination": "self",
                            "response": 304,
                        }
                        return sock, response

            elif ansver["action"] == "auth":
                user = ansver["login"]
                with Session(engine) as s:
                    _find_login = s.scalar(
                        SEL(Client).where(
                            Client.login.in_(
                                [
                                    user,
                                ]
                            )
                        )
                    )

                    if (
                        _find_login.password == ansver["hashed_password"]
                        and _find_login.auth_string == ansver["b_stryng"]
                    ):
                        _find_login.is_authenticated = True

                        s.commit()

                        response = {
                            "name": "server",
                            "action": "auth_ok",
                            "time": time.time(),
                            "destination": "self",
                            "auth_state": _find_login.is_authenticated,
                            "response": 200,
                        }
                        return sock, response

                    else:
                        response = {
                            "name": "server",
                            "action": "auth_false",
                            "time": time.time(),
                            "destination": "self",
                            "auth_state": _find_login.is_authenticated,
                            "response": 200,
                        }
                        return sock, response

            else:
                print(ansver)
                raise TypeError


if __name__ == "__main__":
    Server().run_server()
