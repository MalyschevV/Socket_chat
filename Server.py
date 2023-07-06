from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from colorama import *
from datetime import datetime
import random
import tkinter
from tkinter.ttk import Label
from tkinter.scrolledtext import *

init()

client_address = None
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

HOST = ''
PORT = 3333
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
    global client_address
    while True:
        try: client, client_address = SERVER.accept()
        except socket.error:
            pass
        else:
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            connection = f"пользователь с портом {client_address[1]} подключился к чату."
            print(random.choice(colors) + "["+date_now+"]" + " " + connection)
            client.send(bytes("Дорбо пожаловать в сетевой чат, пожалуйста, введите свой никнейм!\n", "utf8"))
            print(random.choice(colors) + "["+date_now+"]" + " " + connection)
            client.send(bytes("Дорбо пожаловать в сетевой чат, пожалуйста, введите свой никнейм!\n", "utf8"))
            Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    try:
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name = client.recv(BUFSIZ).decode("utf8")
        welcome ='Добро пожаловать %s! Если вы хотите выйти, нажмите на выход.\n' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s Присоединился к чату!\n" % name
        broadcast(bytes(msg, "utf8"),client)
        clients[client] = name
    except:
        del addresses[client]
        disconnection = f"пользователь с портом {client_address[1]} покинул чат."
        print(random.choice(colors) + "["+date_now+"]" + " " + disconnection)
        print(random.choice(colors) + "Текущий онлайн сервера:" + str(len(addresses)))
        return
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, client, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            del addresses[client]
            disconnection = f"пользователь с портом {client_address[1]} покинул чат."
            print(random.choice(colors) + "["+date_now+"]" + " " + disconnection)
            print(random.choice(colors) + "Текущий онлайн сервера:" + str(len(addresses)))
            broadcast(bytes("%s Покинул чат.\n" % name, "utf8"), client)
            break

def broadcast(msg, msg_from, prefix=""):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = msg.decode("utf-8")
    if msg[0] == ">":
        nickname = msg[1:msg.find(" ")]
        msg = msg[msg.find(" "):]
        if nickname in clients.values():
            client_to = list(clients.keys())[list(clients.values()).index(nickname)]
            client_to.send(bytes("["+date_now +"]" + "Вам от " + prefix + msg, "utf8"))
            msg_from.send(bytes("["+date_now +"]" + "Вы отправили для " + nickname + ": " + msg, "utf8"))
            return
    for sock in clients:
        sock.send(bytes("["+date_now +"]" + " " + prefix +msg, "utf8"))

clients = {}
addresses = {}

if __name__ == "__main__":
    SERVER.listen(5)
    print("Ожидание подключения пользователей...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
