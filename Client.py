from ast import Import
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter.ttk import Label
from colorama import *
from datetime import datetime

init()

BUFSIZ = 1024
client_socket = None

def receive():
    global client_socket
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break

def send(event=None):
    global client_socket
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    global client_socket
    my_msg.set("{quit}")
    send(client_socket)

def getPort():
    p = port.get()

top = tkinter.Tk()
top.title("Мессенджер")
top.geometry("460x600")
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=30, width=75, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()
entry_field = tkinter.Entry(top, width=35, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(padx =20, pady = 20, side=tkinter.RIGHT)
send_button = tkinter.Button(top, text="Отправить", width=15, command=send)
send_button.place(x = 225, y= 500)
get_port = tkinter.Button(top, text = "Ввести", command=lambda: establish_connection())
get_port.place(x = 140, y = 555)
host = tkinter.Entry(top)
host.insert(tkinter.END, "127.0.0.1")
host.place(x = 10, y = 515)
port = tkinter.Entry(top)
port.place(x= 10, y = 558)
text = tkinter.Label(text = "Хост:")
text.place(x = 12, y = 490)
p_text = tkinter.Label(text = "Порт:")
p_text.place(x = 12, y = 535)
top.protocol("WM_DELETE_WINDOW", on_closing)

def establish_connection():
    global client_socket
    port = getPort()
    if not port:
        port = 3333
    else:
        port = int(port)
        host = "127.0.0.1"
        ADDR = (host, port)
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDR)
        receive_thread = Thread(target=receive)
        receive_thread.start()

tkinter.mainloop()
