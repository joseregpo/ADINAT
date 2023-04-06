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
                afk(sock_fille)
            case "btk":
                btk(sock_fille)
            case "users":
                users(sock_fille)
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
                sock_fille.sendall("400".encode())

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
    print(state)
    if state == "btk":
        sock_fille.sendall("416".encode())
    elif state == "afk":
        sock_fille.sendall("415".encode())
    elif len(mess) != 2:
        sock_fille.sendall("403".encode())
    else:
        username = mess[1]
        usernameIsTaken = verifyUsernameIsNotAlreadyTaken(username)
        if not usernameIsTaken:
            user = User(username, sock_fille)
            user.setState("btk")
            users.append(user)
            signupFromSrv(username, sock_fille)
            sock_fille.sendall("200".encode())
        else:
            sock_fille.sendall("425".encode())

def signupFromSrv(username, sock_fille):
    for i in range (len(users)):
        sock = users[i].getSocket()
        if sock_fille != sock:
            sock.sendall(("signupFromSrv|"+username).encode())



def msg(mess, sock_fille):
    state = getState(sock_fille)
    print(mess)
    if state == "afk":
        sock_fille.sendall("415".encode())
    else:
        username = getUsername(sock_fille)
        if len(mess) != 1:
            sock_fille.sendall("403".encode())
        else:
            msgFromSrv(username, mess, sock_fille)
            sock_fille.sendall("200".encode())

def msgFromSrv(username, message, sock_fille):
    for i in range (len(users)):
        sock = users[i].getSocket()
        if sock_fille != sock:
            sock.sendall(("msgFromSrv|"+username+"|"+message).encode())



def msgpv(mess, sock_fille):
    state = getState(sock_fille)
    if state == "afk":
        sock_fille.sendall("415".encode())
    else:
        username = getUsername(sock_fille)
        mess = mess.split(" ", 1)
        dest = mess[0]
        message = mess[1]


def exit(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def afk(sock_fille):
    for i in range (len(users)):
        if users[i].getSocket() == sock_fille:
            users[i].setState("afk")
            break

    afkFromSrv(sock_fille)
    sock_fille.sendall("200".encode())

def afkFromSrv(sock_fille):
    username = getUsername(sock_fille)
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            sock_fille.sendall(("afkFromSrv|"+username).encode())


def btk(sock_fille):
    for i in range (len(users)):
        if users[i].getSocket() == sock_fille:
            users[i].setState("btk")
            break

    btkFromSrv(sock_fille)
    sock_fille.sendall("200".encode())

def btkFromSrv(sock_fille):
    username = getUsername(sock_fille)
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            sock_fille.sendall(("btkFromSrv|"+username).encode())

def users(sock_fille):
    usersname = getAllUsersname(sock_fille)
    print(usersname)
    sock_fille.sendall(usersname.encode())

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
        if users[i].getSocket() == sock_fille:
            return users[i].getUsername()
    return None

def getAllUsersname(sock_fille):
    allUsersname = []
    username = getUsername(sock_fille)
    for i in range (len(users)):
        if users[i].getUsername() != username:
            allUsersname.append(users[i].getUsername())

    return allUsersname  
        
def getState(sock_fille):
    for i in range (len(users)):
        if users[i].getSocket() == sock_fille:
            return users[i].getState()
    return None
        
def verifyUsernameIsNotAlreadyTaken(username):
    for i in range (len(users)):
        if users[i].getUsername() == username:
            return True
    return False



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
    if t != threading.main_thread(): 
        t.join
    
sys.exit(0)
