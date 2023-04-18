import socket
import sys
import os
import threading
from datetime import datetime
from user import User
import signal
import traceback
import logging
import configparser

signal.signal(signal.SIGINT, signal.SIG_DFL)

def traiter_client(sock_fille):
    global able_to_use
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
                        with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            signup(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} signup ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "msg":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            msg(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} msg ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "msgpv":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            msgpv(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} msgpv ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "exit":
                     with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            exit(sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                case "afk":
                     with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            afk(sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                case "btk":
                     with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            btk(sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                case "users":
                     with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            getUsers(sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                case "rename":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            rename(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} rename ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "ping":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            ping(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} ping ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "channel":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            channel(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} channel ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "acceptchannel":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            acceptchannel(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} acceptchannel ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "declinechannel":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            declinechannel(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} declinechannel ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "sharefile":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            sharefile(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} sharefile ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "acceptfile":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            acceptfile(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} acceptfile ${dt} 403")
                        sock_fille.sendall("403".encode())
                case "declinefile":
                    if len(mess) != 1:
                         with lock_general:
                            cond_general.wait_for(lambda: able_to_use)
                            able_to_use = False
                            declinefile(mess, sock_fille)
                            able_to_use = True
                            cond_general.notify_all()
                    else:
                        username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        write_to_log_file(f"{username} declinefile ${dt} 403")
                        sock_fille.sendall("403".encode())
                case other:
                    username = getUsername(sock_fille) if getUsername(sock_fille) != None else sock_fille.getsockname()[0]
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username} unknown command ${dt} 400")
                    #sock_fille.sendall(("400|"+allCommands).encode())
        except Exception as e:
            logging.error(traceback.format_exc())
            break

def help(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    if state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username} help ${dt} 430")
        sock_fille.sendall("430".encode())
    else:
        helpFromSrv(sock_fille)
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username} help ${dt} 200")
        sock_fille.sendall("200".encode())

def helpFromSrv(sock_fille):
    sock_fille.sendall(("helpFromSrv|"+allCommands).encode())



def signup(mess, sock_fille):
    connected = getConnected(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    if connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} signup ${dt} 417")
        sock_fille.sendall("417".encode())
    elif len(mess) != 2:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} signup ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        username = mess[1]
        if not username.isalpha():
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} signup ${dt} 426")
            sock_fille.sendall("426".encode())
        else:
            usernameIsTaken = verifyUsernameIsNotAlreadyTaken(username)
            if not usernameIsTaken:
                user = User(username, sock_fille, "btk", True)
                users.append(user)
                signupFromSrv(username, sock_fille)
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} signup ${dt} 200")
                sock_fille.sendall("200".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} signup ${dt} 425")
                sock_fille.sendall("425".encode())

def signupFromSrv(username, sock_fille):
    for i in range (len(users)):
        sock = users[i].getSocket()
        if sock_fille != sock:
            sock.sendall(("signupFromSrv|"+username).encode())



def msg(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} msg ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} msg ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 2:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} msg ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        username = getUsername(sock_fille)
        msgFromSrv(username, mess[1], sock_fille)
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} msg ${dt} 200")
        sock_fille.sendall("200".encode())

def msgFromSrv(username, message, sock_fille):
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("msgFromSrv|"+username+"|"+message).encode())



def msgpv(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    mess = mess[1].split(" ", 1)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]


    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} msgpv ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} msgpv ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 2:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} msgpv ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        
        dest_username = mess[0]
        dest_user = getUserByUsername(dest_username)
        if dest_user is not None:
            if dest_username != username_or_ip:
                channelExists = verifyChannelExists(sock_fille, dest_user)
                if channelExists:
                    my_username = getUsername(sock_fille)
                    message = mess[1]
                    msgpvFromSrv(dest_user, message, my_username)
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username_or_ip} msgpv ${dt} 200")
                    sock_fille.sendall("200".encode())            
                else:
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username_or_ip} msgpv ${dt} 421")
                    sock_fille.sendall("421".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} msgpv ${dt} 407")
                sock_fille.sendall("407".encode())
        else:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} msgpv ${dt} 402")
            sock_fille.sendall("402".encode())

def msgpvFromSrv(dest_user, message, username):
    dest_user.getSocket().sendall(("msgpvFromSrv|"+username+"|"+message).encode())

def afk(sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} afk ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} afk ${dt} 415")
        sock_fille.sendall("415".encode())
    else:
        i = 0
        while i < len(users):
            if users[i].getSocket() == sock_fille:
                users[i].setState("afk")
                break
            i += 1

        afkFromSrv(sock_fille)
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} afk ${dt} 200")
        sock_fille.sendall("200".encode())

def afkFromSrv(sock_fille):
    username = getUsername(sock_fille)
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("afkFromSrv|"+username).encode())


def btk(sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} btk ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "btk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} btk ${dt} 416")
        sock_fille.sendall("416".encode())
    else:
        i = 0
        while i < len(users):
            if users[i].getSocket() == sock_fille:
                users[i].setState("btk")
                break
            i += 1

        btkFromSrv(sock_fille)
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} btk ${dt} 200")
        sock_fille.sendall("200".encode())

def btkFromSrv(sock_fille):
    username = getUsername(sock_fille)
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("btkFromSrv|"+username).encode())

def getUsers(sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} users ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} users ${dt} 430")
        sock_fille.sendall("430".encode())
    else:
        usersname = getAllUsersname(sock_fille)
        getUsersFromSrv(sock_fille, usersname)
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} users ${dt} 200")
        sock_fille.sendall("200".encode())

def getUsersFromSrv(sock_fille, usersname):
    sock_fille.sendall(("usersFromSrv|"+str(usersname)).encode())

def rename(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    mess = mess[1].split(" ")
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} rename ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} rename ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} rename ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        new_username = mess[0]
        if new_username.isalpha():
            usernameIsAvailable = verifyUsernameIsNotAlreadyTaken(new_username)
            if not usernameIsAvailable:
                user = getUser(sock_fille)
                old_username = user.getUsername()
                user.setUsername(new_username)
                renameFromSrv(old_username, new_username, sock_fille)
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} rename ${dt} 200")
                sock_fille.sendall("200".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} rename ${dt} 425")
                sock_fille.sendall("425".encode())
        else:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} rename ${dt} 426")
            sock_fille.sendall("426".encode())

def renameFromSrv(old_username, new_username, sock_fille):
    for i in range (len(users)):
        if users[i].getSocket() != sock_fille:
            users[i].getSocket().sendall(("renameFromSrv|"+str(old_username)+"|"+str(new_username)).encode())

def ping(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    mess = mess[1].split(" ")
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} ping ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} ping ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} ping ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        username = getUsername(sock_fille)
        dest_user = getUserByUsername(mess[0])
        if dest_user is not None:
            if dest_user.getUsername() != username:
                pingFromSrv(dest_user, username)
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} ping ${dt} 200")
                sock_fille.sendall("200".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} ping ${dt} 402")
                sock_fille.sendall("402".encode())
        else:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} ping ${dt} 402")
            sock_fille.sendall("402".encode())

def pingFromSrv(dest_user, username):
    dest_user.getSocket().sendall(("pingFromSrv|"+username).encode())

def channel(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    mess = mess[1].split(" ")
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} channel ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} channel ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} channel ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        my_user = getUser(sock_fille)
        if my_user.getUsername() == mess[0]:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} channel ${dt} 407")
            sock_fille.sendall("407".encode())
        else:
            dest_user = getUserByUsername(mess[0])
            user = getUser(sock_fille)
            if dest_user is not None:
                user_exists_in_dest_user_request_channel = dest_user.checkIfUserExistsInRequestChannel(user)
                dest_user_exists_in_user_request_channel = user.checkIfUserExistsInRequestChannel(dest_user)
                dest_user_exists_in_user_channel = user.checkIfUserExistsInChannel(dest_user)
                if dest_user_exists_in_user_channel:
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username_or_ip} channel ${dt} 404")
                    sock_fille.sendall("404".encode())
                elif user_exists_in_dest_user_request_channel:
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username_or_ip} channel ${dt} 441")
                    sock_fille.sendall("441".encode())
                elif dest_user_exists_in_user_request_channel:
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username_or_ip} channel ${dt} 447")
                    sock_fille.sendall("447".encode())
                else:
                    channelFromSrv(dest_user, user)
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username_or_ip} channel ${dt} 200")
                    sock_fille.sendall("200".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} channel ${dt} 402")
                sock_fille.sendall("402".encode())        

def channelFromSrv(dest_user, user):
    dest_user.addUserToRequestChannel(user)
    dest_user.getSocket().sendall(("channelFromSrv|"+dest_user.getUsername()+"|"+user.getUsername()).encode())

def acceptchannel(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    mess = mess[1].split(" ")
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} acceptchannel ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} acceptchannel ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} acceptchannel ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        sender = getUserByUsername(mess[0])
        user = getUser(sock_fille)
        if sender is not None:
            userRequestChannel = user.getRequestChannel()
            if sender in userRequestChannel:
                user.addUserToChannel(sender)
                user.removeUserFromRequestChannel(sender)
                sender.addUserToChannel(user)
                acceptedchannelFromSrv(sender, user)
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} acceptchannel ${dt} 200")
                sock_fille.sendall("200".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} acceptchannel ${dt} 444")
                sock_fille.sendall("444".encode())
        else:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} acceptchannel ${dt} 402")
            sock_fille.sendall("402".encode())

def acceptedchannelFromSrv(sender, user):
    sender.getSocket().sendall(("acceptedchannelFromSrv|"+user.getUsername()).encode())


def declinechannel(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    mess = mess[1].split(" ")
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} declinechannel ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} declinechannel ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 1:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} declinechannel ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        sender = getUserByUsername(mess[0])
        user = getUser(sock_fille)
        if sender is not None:
            userRequestChannel = user.getRequestChannel()
            if sender in userRequestChannel:
                declinedchannelFromSrv(sender, user)
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} declinechannel ${dt} 200")
                sock_fille.sendall("200".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} declinechannel ${dt} 444")
                sock_fille.sendall("444".encode())
        else:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} declinechannel ${dt} 402")
            sock_fille.sendall("402".encode())


def declinedchannelFromSrv(sender, user):
    user.removeUserFromRequestChannel(sender)
    sender.getSocket().sendall(("declinedchannelFromSrv|"+user.getUsername()).encode())

def sharefile(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    mess = mess[1].split(" ")
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} sharefile ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} sharefile ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 4:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} sharefile ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        user = getUser(sock_fille)
        if user.getUsername() == mess[0]:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} sharefile ${dt} 407")
            sock_fille.sendall("407".encode())
        else: 
            dest_user = getUserByUsername(mess[0])
            if dest_user is not None:
                file_already_in_request_share_file_list = dest_user.checkIfFileExistsInRequestShareFile(user, mess[1])
                if not file_already_in_request_share_file_list:
                    share_file_from_srv(dest_user, user, mess[3], mess[1], mess[2]) 
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username_or_ip} sharefile ${dt} 200")
                    sock_fille.sendall("200".encode())
                else:
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    write_to_log_file(f"{username_or_ip} sharefile ${dt} 442")
                    sock_fille.sendall("442".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} sharefile ${dt} 402")
                sock_fille.sendall("402".encode()) 

def share_file_from_srv(dest_user, user, file_size, file_name, port):
    user.addToRequestSharefile(dest_user, file_name)
    dest_user.addToRequestSharefile(user, file_name)
    adr_src = user.getSocket()
    sockt = adr_src.getsockname()
    dest_user.getSocket().sendall(("sharefileFromSrv|"+str(user.getUsername())+"|"+str(file_name)+"|"+str(file_size)+"|"+str(sockt[0])+"|"+str(port)+"|"+str(sockt[1])).encode())

def acceptfile(mess, sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    mess = mess[1].split(" ")
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} acceptfile ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} acceptfile ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 2:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} acceptfile ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        sender = getUserByUsername(mess[0])
        user = getUser(sock_fille)
        if sender is not None:
            userRequestSharefile = user.getRequestSharefile()
            if sender in userRequestSharefile:
                acceptedfileFromSrv(sender, user, mess[1])
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} acceptfile ${dt} 200")
                sock_fille.sendall("200".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} acceptfile ${dt} 443")
                sock_fille.sendall("443".encode())
        else:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} acceptfile ${dt} 402")
            sock_fille.sendall("402".encode())

def acceptedfileFromSrv(sender, user, file):
    user.removeFromRequestSharefile(sender, file)
    user.addToSharefile(sender, file)
    sender.getSocket().sendall(("acceptedfileFromSrv|"+user.getUsername()+"|"+str(file)).encode())

def declinefile(mess, sock_fille):    
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    mess = mess[1].split(" ")
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} declinefile ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} declinefile ${dt} 430")
        sock_fille.sendall("430".encode())
    elif len(mess) != 2:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} declinefile ${dt} 403")
        sock_fille.sendall("403".encode())
    else:
        sender = getUserByUsername(mess[0])
        user = getUser(sock_fille)
        if sender is not None:
            userRequestSharefile = user.getRequestSharefile()
            if sender in userRequestSharefile:
                declinedFileFromSrv(sender, user, mess[1])
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} declinefile ${dt} 200")
                sock_fille.sendall("200".encode())
            else:
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                write_to_log_file(f"{username_or_ip} declinefile ${dt} 443")
                sock_fille.sendall("443".encode())
        else:
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            write_to_log_file(f"{username_or_ip} declinefile ${dt} 402")
            sock_fille.sendall("402".encode())

def declinedFileFromSrv(sender, user, file):
    user.removeFromRequestSharefile(sender, file)
    sender.getSocket().sendall(("declinedfileFromSrv|"+user.getUsername()).encode())

def exit(sock_fille):
    connected = getConnected(sock_fille)
    state = getState(sock_fille)
    username_or_ip = getUsername(sock_fille) if connected else sock_fille.getsockname()[0]
    if not connected:
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} exit ${dt} 418")
        sock_fille.sendall("418".encode())
    elif state == "afk":
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} exit ${dt} 430")
        sock_fille.sendall("430".encode())
    else:
        user = getUser(sock_fille)
        removeFromUserslist(user)
        exitFromSrv(sock_fille, user.getUsername())
        dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        write_to_log_file(f"{username_or_ip} exit ${dt} 200")
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


def write_to_log_file(text_to_write):
    global able_to_write
    with lock_write_file:
        cond_write_file.wait_for(lambda: able_to_write)
        able_to_write = False
        with open(log_file_name, "a") as server_file:
            server_file.write(text_to_write + "\n")
        able_to_write = True
        cond_write_file.notify_all()
        


users = []

allCommands = "signup <username> : allows you to login into the chatroom\n msg <message> : sends a message in the global chatroom,\n msgpv <username>  <user> : sends a message to someone,\n exit : allows you to leave the chatroom,\n afk : avoid you to sends message in the chatroom,\n btk : allows you to send message in the chatroom if you were afk,\n users : Notifies which clients are connected to the server,\n rename <username> : allows you to change your name,\n ping <username> : sends a ping to a user,\n channel <username> : demands the specified user to create a private channel with him,\n acceptchannel <username> : accept the channel creation demand,\n declinechannel <username> : refuse the channel creation demand,\n sharefile <username> <namefile> : Share a file to someone but he has to accept,\n acceptfile <username> <namefile> : accept the file that has been shared by a user,\n declinefile <username> <namefile> : refuse the file that has been shared by a user\n"

lock_write_file = threading.Lock()
cond_write_file = threading.Condition(lock_write_file)
able_to_write = True

lock_general = threading.Lock()
cond_general = threading.Condition(lock_general)
able_to_use = True

config = configparser.ConfigParser()
config.read('adinat.conf')

port = config.get("server", "port")
log_file_name = config.get("log", "filename")


with socket.socket() as sock_locale:
    sock_locale.bind(("", int(port)))
    sock_locale.listen(4)
    
    while True:
        try:
            sock_client, adr_client = sock_locale.accept()
            threading.Thread(target=traiter_client,
            args=(sock_client,)).start()
        except KeyboardInterrupt:
            break

for t in threading.enumerate():
    if t != threading.main_thread(): 
        t.join
    
sys.exit(0)
