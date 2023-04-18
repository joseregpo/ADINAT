import socket
import sys
import threading
import os
import traceback
import logging
import tqdm
import signal
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
import sys 
from IHM import Ui_DISCUSSIT

signal.signal(signal.SIGINT, signal.SIG_DFL)

#Traitements du serveur
adresse, port = sys.argv[1].split(":")
commands_from_srv = ["signupFromSrv", "helpFromSrv", "msgFromSrv", "msgpvFromSrv", "exitedFromSrv", "afkFromSrv", "btkFromSrv", "usersFromSrv", "renameFromSrv", "pingFromSrv", "channelFromSrv", "acceptedchannelFromSrv", "declinedchannelFromSrv", "sharefileFromSrv", "acceptedfileFromSrv", "declinedfileFromSrv", ]
reponses_possibles = {
    "200" : "Success",
    "400": "The command doesn’t exist probably due to a typing error",
    "401": "Message error",
    "402": "Username does not exist",
    "403": "Wrong numbers of parameters",
    "404": "Private channel already exists",
    "405": "File name does not exist",
    "406": "The name of the file given by the user isn’t corresponding",
    "407": "You are not authorized to send messages to yourself",
    "415": "Already afk",
    "416": "Already btk",
    "417": "User already logged in",
    "418": "User must be logged in",
    "421": "Private channel does not exist",
    "425": "Username already taken",
    "426": "Username must not contain special characters or numbers",
    "430": "User is afk",
    "441": "You have already sent a private channel request to that user",
    "442": "You have already sent a file transfer request to that user",
    "443": "You have no pending share file request from that user",
    "444": "You have no pending private channel request from that user",
    "446": "Not a valid port",
    "447": "There is already a pending private channel request from that user",
    "448": "You are not authorized to send files to yourself:",
    "500": "Internal server error"
}

#Partie stockage utilisateur
username = ""
last_command = ""
connected_users = ["General"]
file_queue = {}
file_reception_requests = {}
chatrooms = {"General" : []}
state = ""

####################  Methodes du serveur Client ASCII


def listen_server_cmd(sock):
    global last_command, username, reponses_possibles, commands_from_srv
    with sock:
        while True:
            try:
                reponse = sock.recv(1024)
                reponse = reponse.decode()
                r_formatted = reponse.split("|")
                #Traitement des messages constants du serveur
                if r_formatted[0] != "200" and r_formatted[0] in reponses_possibles.keys():
                    print(r_formatted[0] + " : " + reponses_possibles[r_formatted[0]])
                else:
                    if r_formatted[0] not in commands_from_srv:
                        command = last_command.split(' ')
                        match command[0]:
                            case "help":
                                pass
                            case "signup":
                                username = last_command.split(" ", 1)
                                username = username[1]
                                print("You are now connected")
                            case "msg":
                                print("Message envoyé")
                                add_to_chat("General", f"{username} : {command[1]}")

                            case "msgpv":
                                add_to_chat(command[1], f"{username} : {command[2]}")
                                print("Message privé envoyé")

                            case "exit":
                                add_to_chat("General", "You are now offline")
                                print("You are now offline")
                                break
                            case "afk":
                                add_to_chat("General", "You are now AFK")
                                print("You are now afk")
                            case "btk":
                                add_to_chat("General", "You are now BTK")
                                print("You are now btk")
                            case "users":
                                print("Request successfully sent")
                            case "rename":
                                username = last_command.split(" ", 1)
                                username = username[1]
                                print("You have been renamed")
                            case "ping":
                                print("You pinged someone")
                                add_to_chat("General", "You pinged someone")
                            case "channel":
                                add_to_chat("General", "Your request for a private channel has been sent")
                                print("Your request for a private channel has been sent")
                            case "acceptchannel":
                                add_to_chat("General", "Your request channel has been accepted")
                                print("Your request channel has been accepted")
                            case "declinechannel":
                                add_to_chat("General", "Your request channel has been declined")
                                print("Your request channel has been declined")
                            case "sharefile":
                                add_to_chat("General", "Your request to send a file  has been sent")
                                print("Your request to send a file  has been sent")
                            case "acceptfile":
                                add_to_chat("General", "Your file accept has been sent")
                                print("Your file accept has been sent")
                            case "declinefile":
                                add_to_chat("General", "Your file denial has been sent")
                                print("Your file denial has been sent")
                            case other:
                                print(f"Sadly, we don't know yet how to manage this response from the server")
                    else :
                        match r_formatted[0]:
                            case "helpFromSrv":
                                print(r_formatted[1])
                            case "signupFromSrv":
                                print(f"{r_formatted[1]} has arrived to the server !")
                                add_to_chat("General", f"{r_formatted[1]} has arrived to the server !")

                                if r_formatted[1] not in connected_users:
                                    connected_users.append(r_formatted[1])

                            case "msgFromSrv":
                                print("Général : " + r_formatted[1] + " : " + r_formatted[2])
                                add_to_chat("General", f"{r_formatted[1]} : {r_formatted[2]}")

                            case "msgpvFromSrv":
                                add_to_chat(r_formatted[1], f"{r_formatted[1]} : {r_formatted[2]}")
                                print("Privé : " + r_formatted[1] + " : " + r_formatted[2])

                            case "exitedFromSrv":
                                print(f"{r_formatted[1]} has exited the server")
                                if r_formatted[1] not in connected_users:
                                    connected_users.remove(r_formatted[1])
                                add_to_chat("General", f"{r_formatted[1]} has exited the server")

                            case "afkFromSrv":
                                print(f"{r_formatted[1]} is now afk")
                                add_to_chat("General", f"{r_formatted[1]} is now afk")

                            case "btkFromSrv":
                                print(f"{r_formatted[1]} is back to the party !")
                                add_to_chat("General", f"{r_formatted[1]} is back to the party !")

                            case "usersFromSrv":
                                print(f"Liste des utilisateurs {r_formatted[1]}")
                                update_users_list(r_formatted[1])

                            case "renameFromSrv":
                                print(f"{r_formatted[1]} changed his name to {r_formatted[2]}")
                                add_to_chat("General", f"{r_formatted[1]} changed his name to {r_formatted[2]}")

                            case "pingFromSrv":
                                print(f"{r_formatted[1]} is looking for you")
                                add_to_chat("General", f"{r_formatted[1]} is looking for you")

                            case "channelFromSrv":
                                print(f"{r_formatted[2]} wants to be private with you")
                                add_to_chat("General", f"{r_formatted[2]} wants to be private with you")

                            case "acceptedchannelFromSrv":
                                add_to_chat("General", f"{r_formatted[1]} has accepted your channel !")
                                print(f"{r_formatted[1]} has accepted your channel")

                            case "declinedchannelFromSrv":
                                print(f"{r_formatted[1]} doesn't want to be alone with you :( ")
                                add_to_chat("General", f"{r_formatted[1]} doesn't want to be alone with you :(")

                            case "sharefileFromSrv":
                                print(f"{r_formatted[1]} wants to send you a file")
                                share_file_from_srv(r_formatted)
                                add_to_chat("General", f"{r_formatted[1]} wants to send you a file")

                            case "acceptedfileFromSrv":
                                print(f"{r_formatted[1]} has accepted to receive your file")
                                add_to_chat("General", f"{r_formatted[1]} has accepted to receive your file")
                                print(f"your file is being sent")
                                accept_file_from_srv_v2(r_formatted)

                            case "declinedfileFromSrv":
                                print(f"{r_formatted[1]} doesn't want files from you D: ")
                                add_to_chat("General", f"{r_formatted[1]} doesn't want files from you D: ")
            except Exception as e:
                logging.error(traceback.format_exc())

def update_users_list(users_string):
    global connected_users
    users_string = users_string.replace("[","")
    users_string = users_string.replace("]","")
    users_string = users_string.replace("'","")
    users_string = users_string.replace(" ","")
    connected_users = users_string.split(",")
    print(connected_users)
    # print(users_string[1:len(users_string)-1])

def renameFromSrv(r_formatted):
    global file_queue, file_reception_requests, chatrooms
    old_username = r_formatted[1]
    new_username = r_formatted[2]
    rename_in_dico(old_username,new_username,file_queue)
    rename_in_dico(old_username,new_username,file_reception_requests)
    rename_in_dico(old_username,new_username,chatrooms)

def add_to_chat(nom_chat, msg):
    global chatrooms
    if nom_chat in chatrooms.keys():
        chatrooms[nom_chat].extend([msg])
    else :
        chatrooms[nom_chat] = [msg]

def rename_in_dico(old_key, new_key, dico):
    for k,v in dico.items():
        if k == old_key:
            try:
                dico[new_key] = dico.pop(old_key)
            except Exception as e:
                logging.error(traceback.format_exc())

def check_port_availability(sock, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((sock.getsockname()[0], int(port)))
        return True
    except Exception as e:
        logging.error(traceback.format_exc())
        return False

def check_file_path(path):
    return os.path.exists(path)

def send_file(r_formatted):
    global file_queue
    user = r_formatted[1]
    file_name = r_formatted[2]
    file_stats = os.stat(file_name)
    progress = tqdm.tqdm(range(file_stats.st_size), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
    for u, (f, sock) in file_queue.items():
        s_target, _ = sock.accept()
        if u == user and f == file_name:
            with open(file_name, "rb") as f:
                while True:
                    bytes_read = f.read(4096)
                    if not bytes_read:
                        break
                    s_target.sendall(bytes_read)
                    progress.update(len(bytes_read))

def accept_file_from_srv_v2(r_formatted):
    # A thread for each file we send
    threading.Thread(target=send_file, args=(r_formatted,)).start()
    for t in threading.enumerate():
        if t != threading.main_thread(): 
            t.join

def prepare_share_file(sock, m_formatted):
    global file_queue
    f_path = m_formatted[2]
    file_stats = os.stat(f_path)
    f_name = os.path.basename(f_path)

    #A Socket for each file to send
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((sock.getsockname()[0], int(m_formatted[3])))
    s.listen(4)
    # Dict of all files to send
    if m_formatted[1] in file_queue.keys():
        file_queue[m_formatted[1]].extend([f_path, s])
    else:
        file_queue[m_formatted[1]] = [f_path, s]
    return f"sharefile {username} {f_name} {m_formatted[3]} {file_stats.st_size}"

def share_file_from_srv(m_formatted):
    global file_reception_requests
    username = m_formatted[1]
    file_name = m_formatted[2]
    f_size = m_formatted[3]
    target_ip = m_formatted[4]
    target_port = m_formatted[5]
    if username in file_reception_requests.keys():
        file_reception_requests[username].extend([(file_name, f_size, target_ip, target_port)])
    else:
        file_reception_requests[username] = [(file_name, f_size, target_ip, target_port)]

def accept_file(response_formatted):
    user = response_formatted[1]
    file = response_formatted[2]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for u, f in file_reception_requests.items():
        if u == user and file == f[0][0]:
            size = f[0][1]
            adr_ip = f[0][2]
            port = f[0][3]
            s.connect((str(adr_ip), int(port)))
            threading.Thread(target=wait_for_file_arrival, args=(s, size, user, file)).start()
            for t in threading.enumerate():
                if t != threading.main_thread(): 
                    t.join

def wait_for_file_arrival(sock, size, user, file):
    progress = tqdm.tqdm(range(int(size)), f"Receiving {user}", unit="B", unit_scale=True, unit_divisor=1024)
    with sock:
        with open("testfile.jpg", "wb") as f:
        # with open(file, "wb") as f:
            while True:
                try:
                    bytes_read = sock.recv(4096)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                except Exception as e:
                    logging.error(traceback.format_exc())
        sock.shutdown(socket.SHUT_RDWR)
        progress.update(len(bytes_read))
    sys.exit(0)

def talk_to_server(sock):
    global last_command, username
    while True:
        if last_command == "exit":
            break
        cmd = input("$ ")
        last_command = cmd
        temp = cmd.split(" ")
        if temp[0] == "sharefile":
            if check_file_path(temp[2]) and check_port_availability(sock, temp[3]):
                cmd = prepare_share_file(sock, temp)
                sock.sendall(cmd.encode())
            elif not check_file_path(temp[2]):
                print(reponses_possibles["405"])
            elif not check_port_availability(sock, temp[3]):
                print(reponses_possibles["446"])
        elif temp[0] == "acceptfile":
            accept_file(temp)
            sock.sendall(cmd.encode())
        else:
            sock.sendall(cmd.encode())



#################################################################




############   Methodes du IHM
class MainWindow(QWidget, Ui_DISCUSSIT):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.sock_locale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_locale.connect((adresse, int(port)))
        recv_thread = threading.Thread(target=self.listen_server_cmd, args=(self.sock_locale,))
        recv_thread.start()
        for t in threading.enumerate():
            if t != threading.main_thread(): 
                t.join
        self.send_message.clicked.connect(self.on_clic)
        self.users_lists.itemClicked.connect(self.change_chatroom)
        self.chats.addItems(chatrooms["General"])
        self.users_lists.addItems(connected_users)

    def change_chatroom(self, item):
        for k, v in chatrooms.items():
            if k == item.text():
                self.chats.clear()
                self.chats.addItems(v)

    def update_chatroom_by_name(self, chatroom):
        for k, v in chatrooms.items():
            if k == chatroom:
                self.chats.clear()
                self.chats.addItems(v)

    def on_clic(self):
        self.talk_to_server_from_IHM(self.message.text())
        self.message.setText("")

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.on_clic()

    def talk_to_server_from_IHM(self, cmd):
        global last_command, username
        if last_command == "exit":
            sys.exit(0)
        last_command = cmd
        temp = cmd.split(" ")
        print(temp)
        if temp[0] == "sharefile":
            if check_file_path(temp[2]) and check_port_availability(self.sock_locale, temp[3]):
                cmd = prepare_share_file(self.sock_locale, temp)
                self.sock_locale.sendall(cmd.encode())
            elif not check_file_path(temp[2]):
                print("405 : ", reponses_possibles["405"])
                last_command = ""
            elif not check_port_availability(self.sock_locale,temp[3]):
                print("446 : ", reponses_possibles["446"])
                last_command = ""
        elif temp[0] == "acceptfile":
            accept_file(temp)
            self.sock_locale.sendall(cmd.encode())
        else:
            self.sock_locale.sendall(cmd.encode())
        # self.sock_locale.sendall("users".encode())
    
    def updateUsersList(self, users_string):
        global connected_users
        users_string = users_string.replace("[","")
        users_string = users_string.replace("]","")
        users_string = users_string.replace("'","")
        users_string = users_string.replace(" ","")
        connected_users = ["General"] + users_string.split(",")
        self.users_lists.clear()
        self.users_lists.addItems(list(connected_users))

    def request_users(self, sec):
        def func_wrapper():
            self.request_users(sec)
            if state != "afk":
                self.sock_locale.sendall("users".encode())
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t


    def add_to_chat(self, nom_chat, msg):
        if nom_chat in chatrooms.keys():
            chatrooms[nom_chat].append(msg)
        else :
            chatrooms[nom_chat] = [msg]
    
    def traiter_state(self, user, state):
        for u in connected_users:
            if u == user:
                if state == "btk":
                    u = u.split(" ")
                    u = u[0]
                elif state == "afk":
                    u += " (afk)"

    def listen_server_cmd(self, sock):
        global last_command, username, reponses_possibles, commands_from_srv, state
        cpteur_reponses = 0
        with sock:
            while True:
                try:
                    cpteur_reponses += 1
                    reponse = sock.recv(1024)
                    reponse = reponse.decode()
                    # print(f"reponse nro : {cpteur_reponses} avec {reponse}")
                    r_formatted = reponse.split("|")
                    #Traitement des messages constants du serveur
                    if r_formatted[0] != "200" and r_formatted[0] in reponses_possibles.keys():
                        print(r_formatted[0] + " : " + reponses_possibles[r_formatted[0]])
                    else:
                        if r_formatted[0] not in commands_from_srv:
                            command = last_command.split(' ')
                            match command[0]:
                                case "help":
                                    self.add_to_chat("General", r_formatted[1])
                                case "signup":
                                    username = last_command.split(" ", 1)
                                    username = username[1]
                                    self.add_to_chat("General", "You are now connected jhsbflhsfdlk")
                                    self.update_chatroom_by_name("General")
                                    self.request_users(2)
                                    state = "btk"

                                case "msg":
                                    self.add_to_chat("General", f"{username} : {command[1]}")
                                    self.update_chatroom_by_name("General")

                                case "msgpv":
                                    temp = command [2:]
                                    msg = ""
                                    for mot in temp:
                                        msg += mot + " "
                                    self.add_to_chat(command[1], f"{username} : {msg}")
                                    self.update_chatroom_by_name(command[1])

                                case "exit":
                                    self.add_to_chat("General", "You are now offline")
                                    self.update_chatroom_by_name("General")
                                    break

                                case "afk":
                                    self.add_to_chat("General", "You are now AFK")
                                    self.update_chatroom_by_name("General")
                                    state = "afk"

                                case "btk":
                                    self.add_to_chat("General", "You are now BTK")
                                    self.update_chatroom_by_name("General")
                                    state = "btk"

                                case "rename":
                                    username = last_command.split(" ", 1)
                                    username = username[1]
                                    self.add_to_chat("General", "You have been renamed")
                                    self.update_chatroom_by_name("General")

                                case "ping":
                                    self.add_to_chat("General", "You pinged someone")
                                    self.update_chatroom_by_name("General")

                                case "channel":
                                    self.add_to_chat("General", "Your request for a private channel has been sent")
                                    self.update_chatroom_by_name("General")

                                case "acceptchannel":
                                    self.add_to_chat("General", "Your request channel has been accepted")
                                    self.update_chatroom_by_name("General")

                                case "declinechannel":
                                    self.add_to_chat("General", "Your request channel has been declined")
                                    self.update_chatroom_by_name("General")

                                case "sharefile":
                                    self.add_to_chat("General", "Your request to send a file  has been sent")
                                    self.update_chatroom_by_name("General")

                                case "acceptfile":
                                    self.add_to_chat("General", "Your file accept has been sent")
                                    self.update_chatroom_by_name("General")

                                case "declinefile":
                                    self.add_to_chat("General", "Your file denial has been sent")
                                    self.update_chatroom_by_name("General")

                                case "users":
                                    pass

                                case "":
                                    pass

                            last_command = ""
                        else :
                            match r_formatted[0]:
                                case "signupFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} has arrived to the server !")
                                    if r_formatted[1] not in connected_users:
                                        connected_users.append(r_formatted[1])
                                    self.update_chatroom_by_name("General")

                                case "msgFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} : {r_formatted[2]}")
                                    self.update_chatroom_by_name("General")

                                case "msgpvFromSrv":
                                    self.add_to_chat(r_formatted[1], f"{r_formatted[1]} : {r_formatted[2]}")
                                    self.update_chatroom_by_name(r_formatted[1])

                                case "exitedFromSrv":
                                    if r_formatted[1] not in connected_users:
                                        connected_users.remove(r_formatted[1])
                                    self.add_to_chat("General", f"{r_formatted[1]} has exited the server")
                                    self.update_chatroom_by_name("General")

                                case "afkFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} is now afk")
                                    self.update_chatroom_by_name("General")

                                case "btkFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} is back to the party !")
                                    self.update_chatroom_by_name("General")

                                case "usersFromSrv":
                                    update_users_list(r_formatted[1])
                                    self.updateUsersList(r_formatted[1])

                                case "renameFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} changed his name to {r_formatted[2]}")
                                    self.updateUsersList(r_formatted[1])
                                    self.update_chatroom_by_name("General")

                                case "pingFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} is looking for you")
                                    self.update_chatroom_by_name("General")

                                case "channelFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[2]} wants to be private with you")
                                    self.update_chatroom_by_name("General")

                                case "acceptedchannelFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} has accepted your channel !")
                                    self.update_chatroom_by_name("General")

                                case "declinedchannelFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} doesn't want to be alone with you :(")
                                    self.update_chatroom_by_name("General")

                                case "sharefileFromSrv":
                                    share_file_from_srv(r_formatted)
                                    self.add_to_chat("General", f"{r_formatted[1]} wants to send you a file")
                                    self.update_chatroom_by_name("General")

                                case "acceptedfileFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} has accepted to receive your file")
                                    accept_file_from_srv_v2(r_formatted)
                                    self.update_chatroom_by_name("General")

                                case "declinedfileFromSrv":
                                    self.add_to_chat("General", f"{r_formatted[1]} doesn't want files from you D: ")
                                    self.update_chatroom_by_name("General")

                except Exception as e:
                    logging.error(traceback.format_exc())


if __name__ == '__main__':
    import sys
    #Socket de connexion au serveur
    # sock_locale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock_locale.connect((adresse, int(port)))
    # recv_thread = threading.Thread(target=listen_server_cmd, args=(sock_locale,))
    # send_thread = threading.Thread(target=talk_to_server, args=(sock_locale,))
    # On lance les threads
    # recv_thread.start()
    # send_thread.start()
    # for t in threading.enumerate():
    #     if t != threading.main_thread(): 
    #         t.join

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
