import socket
import sys
import threading
from user import *

def traiter_client(sock_fille):
    while True:
        mess = sock_fille.recv(256)
        mess = mess.decode()
        mess = mess.split(" ", 1)
        
        match mess[0]:
            case "help":
                help(mess, sock_fille)
            case "signup":
                login(mess, sock_fille)
            case "msg":
                msg(mess, sock_fille)
            case "msgpv":
                msgpv(mess, sock_fille)
            case "exit":
                exit(mess, sock_fille)
            case "afk":
                afk(mess, sock_fille)
            case "btk":
                btk(mess, sock_fille)
            case "users":
                users(mess, sock_fille)
            case "rename":
                rename(mess, sock_fille)
            case "ping":
                ping(mess, sock_fille)
            case "channel":
                channel(mess, sock_fille)
            case "acceptchannel":
                acceptchannel(mess, sock_fille)
            case "declinechannel":
                declinechannel(mess, sock_fille)
            case "sharefile":
                sharefile(mess, sock_fille)
            case "acceptfile":
                acceptfile(mess, sock_fille)
            case "declinefile":
                declinefile(mess, sock_fille)
            case other:
                sock_fille.sendall("Unknown command".encode())

def help(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def login(mess, sock_fille):
    if len(mess) != 2:
        sock_fille.sendall("403".encode())
    else:
        username = mess[1]
        user = User(username, sock_fille)
        users.append(user)
        for i in range (len(users)):
            print(users[i])
        sock_fille.sendall("200".encode())

def msg(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def msgpv(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def exit(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def afk(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def btk(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def users(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def rename(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def ping(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def channel(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def acceptchannel(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def declinechannel(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def sharefile(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def acceptfile(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def declinefile(mess, sock_fille):
    sock_fille.sendall(mess.upper())



users = []

with socket.socket() as sock_locale:
    sock_locale.bind(("", int(sys.argv[1])))
    sock_locale.listen(4)
    
    while True:
        try:
            sock_client, adr_client = sock_locale.accept()
            threading.Thread(target=traiter_client,
            args=(sock_client,)).start()
        except KeyboardInterrupt:
            break

print("Bye")



for t in threading.enumerate():
    if t != threading.main_thread(): t.join
    
sys.exit(0)
