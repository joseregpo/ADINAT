import socket
import sys
import threading
from user import *

def traiter_client(sock_fille):
    while True:
        try:
            mess = sock_fille.recv(1024)
            mess = mess.decode()
            mess = mess.split(" ", 1)
            
            match mess[0]:
                case "help":
                    help(mess, sock_fille)
                case "signup":
                    if len(mess) != 1:
                        signup(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "msg":
                    if len(mess) != 1:
                        msg(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "msgpv":
                    if len(mess) != 1:
                        msgpv(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "exit":
                    exit(sock_fille)
                case "afk":
                    afk(sock_fille)
                case "btk":
                    btk(sock_fille)
                case "users":
                    getUsers(sock_fille)
                case "rename":
                    if len(mess) != 1:
                        rename(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "ping":
                    if len(mess) != 1:
                        ping(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "channel":
                    if len(mess) != 1:
                        channel(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "acceptchannel":
                    if len(mess) != 1:
                        acceptchannel(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "declinechannel":
                    if len(mess) != 1:
                        declinechannel(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "sharefile":
                    if len(mess) != 1:
                        sharefile(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "acceptfile":
                    if len(mess) != 1:
                        acceptfile(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case "declinefile":
                    if len(mess) != 1:
                        declinefile(mess, sock_fille)
                    else:
                        sock_fille.sendall("403".encode())
                case other:
                    sock_fille.sendall(("400|"+allCommands).encode())
        except:
            break

def help(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("415".encode())
    else:
        sock_fille.sendall(("200|"+allCommands).encode())



def signup(mess, sock_fille):
    connected = getConnected(sock_fille)

    if connected:
        sock_fille.sendall("417".encode())
    elif len(mess) != 2:
        sock_fille.sendall("403".encode())
    else:
        username = mess[1]
        if not username.isalpha():
            sock_fille.sendall("426".encode())
        else:
            usernameIsTaken = verifyUsernameIsNotAlreadyTaken(username)
            if not usernameIsTaken:
                user = User(username, sock_fille, "btk", True)
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
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    elif len(mess) != 2:
        sock_fille.sendall("403".encode())
    else:
        username = getUsername(sock_fille)
        msgFromSrv(username, mess[1], sock_fille)
        sock_fille.sendall("200".encode())

def msgFromSrv(username, message, sock_fille):
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("msgFromSrv|"+username+"|"+message).encode())



def msgpv(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    mess = mess[1].split(" ", 1)

    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    elif len(mess) != 2:
        sock_fille.sendall("403".encode())
    else:
        
        dest_username = mess[0]
        dest_user = getUserByUsername(dest_username)
        if dest_user is not None:
            channelExists = verifyChannelExists(sock_fille, dest_user)
            if channelExists:
                my_username = getUsername(sock_fille)
                message = mess[1]
                msgpvFromSrv(dest_user, message, my_username)
                sock_fille.sendall("200".encode())            
            else:
                sock_fille.sendall("440".encode())
        else:
            sock_fille.sendall("402".encode())

def msgpvFromSrv(dest_user, message, username):
    dest_user.getSocket().sendall(("msgpvFromSrv|"+username+"|"+message).encode())

def afk(sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("415".encode())
    else:
        i = 0
        while i < len(users):
            if users[i].getSocket() == sock_fille:
                users[i].setState("afk")
                break
            i += 1

        afkFromSrv(sock_fille)
        sock_fille.sendall("200".encode())

def afkFromSrv(sock_fille):
    username = getUsername(sock_fille)
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("afkFromSrv|"+username).encode())


def btk(sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "btk":
        sock_fille.sendall("416".encode())
    else:
        i = 0
        while i < len(users):
            if users[i].getSocket() == sock_fille:
                users[i].setState("btk")
                break
            i += 1

        btkFromSrv(sock_fille)
        sock_fille.sendall("200".encode())

def btkFromSrv(sock_fille):
    username = getUsername(sock_fille)
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("btkFromSrv|"+username).encode())

def getUsers(sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    else:
        usersname = getAllUsersname(sock_fille)
        getUsersFromSrv(sock_fille, usersname)
        sock_fille.sendall("200".encode())

def getUsersFromSrv(sock_fille, usersname):
    sock_fille.sendall(("usersFromSrv|"+str(usersname)).encode())

def rename(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    mess = mess[1].split(" ")
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        sock_fille.sendall("403".encode())
    else:
        new_username = mess[0]
        usernameIsAvailable = verifyUsernameIsNotAlreadyTaken(new_username)
        if not usernameIsAvailable:
            user = getUser(sock_fille)
            old_username = user.getUsername()
            user.setUsername(new_username)
            renameFromSrv(old_username, new_username, sock_fille)
            sock_fille.sendall("200".encode())
        else:
            sock_fille.sendall("425".encode())

def renameFromSrv(old_username, new_username, sock_fille):
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("renameFromSrv|"+str(old_username)+"|"+str(new_username)).encode())

def ping(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    mess = mess[1].split(" ")
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        sock_fille.sendall("403".encode())
    else:
        username = getUsername(sock_fille)
        dest_user = getUserByUsername(mess[0])
        if dest_user is not None:
            pingFromSrv(dest_user, username)
            sock_fille.sendall("200".encode())
        else:
            sock_fille.sendall("402".encode())

def pingFromSrv(dest_user, username):
    dest_user.getSocket().sendall(("pingFromSrv|"+username).encode())

def channel(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    mess = mess[1].split(" ")
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        sock_fille.sendall("403".encode())
    else:
        my_user = getUser(sock_fille)
        if my_user.getUsername() == mess[0]:
            sock_fille.sendall("407".encode())
        else:
            dest_user = getUserByUsername(mess[0])
            if dest_user is not None:
                user = getUser(sock_fille)
                channelFromSrv(dest_user, user)
                sock_fille.sendall("200".encode())
            else:
                sock_fille.sendall("402".encode())        

def channelFromSrv(dest_user, user):
    dest_user.addUserToRequestChannel(user)
    user.addUserToRequestChannel(dest_user)
    dest_user.getSocket().sendall(("channelFromSrv|"+dest_user.getUsername()+"|"+user.getUsername()).encode())

def acceptchannel(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    mess = mess[1].split(" ")
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        sock_fille.sendall("403".encode())
    else:
        sender = getUserByUsername(mess[0])
        user = getUser(sock_fille)
        if sender is not None:
            userRequestChannel = user.getRequestChannel()
            senderRequestChannel = sender.getRequestChannel()
            if sender in userRequestChannel and user in senderRequestChannel:
                user.addUserToChannel(sender)
                user.removeUserFromRequestChannel(sender)
                sender.addUserToChannel(user)
                sender.removeUserFromRequestChannel(user)
                acceptedchannelFromSrv(sender, user)
                sock_fille.sendall("200".encode())
            else:
                sock_fille.sendall("444".encode())
        else:
            sock_fille.sendall("402".encode())

def acceptedchannelFromSrv(sender, user):
    sender.getSocket().sendall(("acceptedchannelFromSrv|"+user.getUsername()).encode())


def declinechannel(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    mess = mess[1].split(" ")
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        sock_fille.sendall("403".encode())
    else:
        sender = getUserByUsername(mess[0])
        user = getUser(sock_fille)
        if sender is not None:
            userRequestChannel = user.getRequestChannel()
            senderRequestChannel = sender.getRequestChannel()
            if sender in userRequestChannel and user in senderRequestChannel:
                declinedchannelFromSrv(sender, user)
                sock_fille.sendall("200".encode())
            else:
                sock_fille.sendall("444".encode())
        else:
            sock_fille.sendall("402".encode())


def declinedchannelFromSrv(sender, user):
    user.removeUserFromRequestChannel(sender)
    sender.removeUserFromRequestChannel(user)
    sender.getSocket().sendall(("declinedchannelFromSrv|"+user.getUsername()).encode())

def sharefile(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def acceptfile(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def declinefile(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def exit(sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    if not connected:
        sock_fille.sendall("418".encode())
    elif state == "afk":
        sock_fille.sendall("430".encode())
    else:
        user = getUser(sock_fille)
        removeFromUserslist(user)
        exitFromSrv(sock_fille, user.getUsername())
        sock_fille.sendall("200".encode())
        sock_fille.close()

def exitFromSrv(sock_fille, username):
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("exitedFromSrv|"+username).encode())





def getUserByUsername(username):
    for i in range(len(users)):
        if users[i].getUsername() == username:
            return users[i]
    return None

def getUser(sock_fille):
    for i in range (len(users)):
        if users[i].getSocket() == sock_fille:
            return users[i]
    return None

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

def getConnected(sock_fille):
    for i in range(len(users)):
        if users[i].getSocket() == sock_fille:
            return users[i].getConnected()
    return False
        
def verifyUsernameIsNotAlreadyTaken(username):
    for i in range (len(users)):
        if users[i].getUsername() == username:
            return True
    return False

def verifyChannelExists(sock_fille, user):
    me = getUser(sock_fille)
    if user in me.getChannel():
        return True
    return False

def removeFromUserslist(user):
    users.remove(user)



users = []

allCommands = "signup <username> : allows you to login into the chatroom\n msg <message> : sends a message in the global chatroom,\n msgpv <username>  <user> : sends a message to someone,\n exit : allows you to leave the chatroom,\n afk : avoid you to sends message in the chatroom,\n btk : allows you to send message in the chatroom if you were afk,\n users : Notifies which clients are connected to the server,\n rename <username> : allows you to change your name,\n ping <username> : sends a ping to a user,\n channel <username> : demands the specified user to create a private channel with him,\n acceptchannel <username> : accept the channel creation demand,\n declinechannel <username> : refuse the channel creation demand,\n sharefile <username> <namefile> : Share a file to someone but he has to accept,\n acceptfile <username> <namefile> : accept the file that has been shared by a user,\n declinefile <username> <namefile> : refuse the file that has benn shared by a user\n"

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
