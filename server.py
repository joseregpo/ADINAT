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
                signup(mess, sock_fille)
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
    state = getState(sock_fille)
    if state == "afk":
        sock_fille.sendall("415".encode())
    else:
        if len(mess) != 1:
            sock_fille.sendall("403".encode())
        else:
            sock_fille.sendall("200|signup <username> : allows you to login into the chatroom\n msg <message> : sends a message in the global chatroom,\n msgpv <username>  <user> : sends a message to someone,\n exit : allows you to leave the chatroom,\n afk : avoid you to sends message in the chatroom,\n btk : allows you to send message in the chatroom if you were afk,\n users : Notifies which clients are connected to the server,\n rename <username> : allows you to change your name,\n ping <username> : sends a ping to a user,\n channel <username> : demands the specified user to create a private channel with him,\n acceptchannel <username> : accept the channel creation demand,\n declinechannel <username> : refuse the channel creation demand,\n sharefile <username> <namefile> : Share a file to someone but he has to accept,\n acceptfile <username> <namefile> : accept the file that has been shared by a user,\n declinefile <username> <namefile> : refuse the file that has benn shared by a user".encode())



def signup(mess, sock_fille):
    state = getState(sock_fille)
    if state == "btk":
        sock_fille.sendall("416".encode())
    else:
        if len(mess) != 2:
            sock_fille.sendall("403".encode())
        else:
            username = mess[1]
            user = User(username, sock_fille)
            users.append(user)
            signupFromSrv(username, sock_fille)
            sock_fille.sendall("200".encode())

def signupFromSrv(username, sock_fille):
    for i in range (len(users)):
        sock = users[i].getSocket()
        if sock_fille != sock:
            sock.sendall("signupFromSrv|"+username)



def msg(mess, sock_fille):
    state = getState(sock_fille)
    if state == "afk":
        sock_fille.sendall("415".encode())
    else:
        username = getUsername(sock_fille)
        if len(mess) != 2:
            sock_fille.sendall("403".encode())
        else:
            message = mess[1]
            msgFromSrv(username, message, sock_fille)
            sock_fille.sendall("200".encode())

def msgFromSrv(username, message, sock_fille):
    for i in range (len(users)):
        sock = users[i].getSocket()
        if sock_fille != sock:
            sock.sendall("msgFromSrv|"+username+"|"+message)



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


def getUsername(sock_fille):
    for i in range (len(users)):
        if users[i].getSocket == sock_fille:
            return users[i].getUsername()
        
def getState(sock_fille):
    for i in range (len(users)):
        if users[i].getSocket == sock_fille:
            return users[i].getState()



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
