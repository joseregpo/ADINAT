import socket
import sys
import threading
import os
import traceback
import logging
import tqdm
import signal


signal.signal(signal.SIGINT, signal.SIG_DFL)

#Traitements du serveur
adresse, port = sys.argv[1].split(":")
commands_from_srv = ["signupFromSrv", "helpFromSrv", "msgFromSrv", "msgpvFromSrv", "exitedFromSrv", "afkFromSrv", "btkFromSrv", "usersFromSrv", "renameFromSrv", "pingFromSrv", "channelFromSrv", "acceptedchannelFromSrv", "declinedchannelFromSrv", "sharefileFromSrv", "acceptedfileFromSrv", "declinedfileFromSrv", ]
reponses_possibles = {
    "200" : "Succes",
    "400" : "The command doesn’t exist probably due to a typing error",
    "401": "Message error",
    "402": "Username does not exist",
    "403": "Wrong numbers of parameters",
    "404": "Private channel already exists",
    "405": "File name does not exist",
    "407": "You are not authorized to send messages to yourself",
    "415": "Already afk",
    "416": "Alredy btk",
    "417": "User already logged in",
    "418": "User must be logged in",
    "421": "Private channel does not exist",
    "425": "Username already taken",
    "426": "Username must not contain special characters or numbers",
    "430": "User if afk",
    "440": "You have no pending private channel requests",
    "441": "You have already sent this requests",
    "500": "Internal server error",
}

#Partie stockage utilisateur
username = ""
last_command = ""
liste_msg = []
liste_msg_pv = []
file_queue = {}
file_reception_requests = {}
#Methodes
def listen_server_cmd(sock):
    global last_command, username, liste_msg, reponses_possibles, commands_from_srv, liste_msg_pv
    with sock:
        while True:
            try:
                reponse = sock.recv(1024)
                reponse = reponse.decode()
                r_formatted = reponse.split("|")
                # if r_formatted[0] != "200" and not r_formatted[0] in reponses_possibles.keys():
                #     print(r_formatted[0])
                    # print(f"{r_formatted[0]} : {reponses_possibles[r_formatted[0]]}")
                # if r_formatted[0] == "200":
                #Traitement des messages constants du serveur

                if r_formatted[0] != "200" and r_formatted[0] in reponses_possibles.keys():
                    print(r_formatted[0] + " : " + reponses_possibles[r_formatted[0]])
                
                else:
                    print(r_formatted)
                    if r_formatted[0] not in commands_from_srv:
                        command = last_command.split(' ')
                        match command[0]:
                            case "help":
                                print(r_formatted[1])
                            case "signup":
                                username = last_command.split(" ", 1)
                                username = username[1]
                                print("You are now connected")
                            case "msg":
                                print("Message envoyé")
                            case "msgpv":
                                print("Message privé envoyé")
                            case "exit":
                                print("You are now offline")
                                break
                            case "afk":
                                print("You are now afk")
                            case "btk":
                                print("You are now btk")
                            case "users":
                                print("Request successfully sent")
                            case "rename":
                                print("You have been renamed")
                            case "ping":
                                print("You pinged someone")
                            case "channel":
                                print("Your request for a private channel has been sent")
                            case "acceptchannel":
                                print("Your request channel has been accepted")
                            case "declinechannel":
                                print("Your request channel has been declined")
                            case "sharefile":
                                prepare_share_file(sock,command)
                                print("Your request to send a file  has been sent")
                            case "acceptfile":
                                accept_file(r_formatted)
                                print("Your file accept has been sent")
                            case "declinefile":
                                print("Your file denial has been sent")
                            case other:
                                print(f"Sadly, we don't know yet how to manage this response from the server")
                    else :
                        match r_formatted[0]:
                            case "signupFromSrv":
                                print(f"{r_formatted[1]} has arrived to the server !")
                            case "msgFromSrv":
                                print("Général : " + r_formatted[1] + " : " + r_formatted[2])
                            case "msgpvFromSrv":
                                print("Privé : " + r_formatted[1] + " : " + r_formatted[2])
                            case "exitedFromSrv":
                                print(f"{r_formatted[1]} has exited the server")
                            case "afkFromSrv":
                                print(f"{r_formatted[1]} is now afk")
                            case "btkFromSrv":
                                print(f"{r_formatted[1]} is back to the party !")
                            case "usersFromSrv":
                                print(f"Liste des utilisateurs {r_formatted[1]}")
                            case "renameFromSrv":
                                print(f"{r_formatted[1]} changed his name to {r_formatted[2]}")
                            case "pingFromSrv":
                                print(f"{r_formatted[1]} is looking for you")
                            case "channelFromSrv":
                                print(f"{r_formatted[2]} wants to be private with you")
                            case "acceptedchannelFromSrv":
                                print(f"{r_formatted[1]} has accepted your channel")
                            case "declinedchannelFromSrv":
                                print(f"{r_formatted[1]} doesn't want to be alone with you :( ")
                            case "sharefileFromSrv":
                                print(f"{r_formatted[1]} wants to send you a file")
                                print(f"{r_formatted}")
                                share_file_from_srv(r_formatted)
                            case "acceptedfileFromSrv":
                                print(f"{r_formatted}")
                                print(f"{r_formatted[1]} has accepted to receive your file")
                                print(f"your file is being sent")
                                send_file(r_formatted)
                            case "declinedfileFromSrv":
                                print(f"{r_formatted[1]} doesn't want files from you D: ")
            except Exception as e:
                logging.error(traceback.format_exc())



def talk_to_server(sock):
    global last_command, username, liste_msg
    while True:
        if last_command == "exit":
            break
        cmd = input("$ ")
        last_command = cmd
        temp = cmd.split(" ")
        if temp[0] == "sharefile":
            cmd += prepare_share_file(temp)
            tmp = cmd
            print(tmp) 
        sock.sendall(cmd.encode())

# sharefile <username> <file path> <port>
def send_file(sock, user, file_name):
    global file_queue
    file_stats = os.stat(file_name)
    progress = tqdm.tqdm(range(file_stats.st_size), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
    for u, f in file_queue.items():
        if u == user and f == file_name:
            with open(file_name, "rb") as f:
                while True:
                    # read the bytes from the file
                    bytes_read = f.read(4096)
                    if not bytes_read:
                        # file transmitting is done
                        break
                    # we use sendall to assure transimission in 
                    # busy networks
                    sock.sendall(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))
    sock.shutdown(socket.SHUT_RDWR)

def accept_file_from_srv(sock, user, file_name):
        
    while True:
        try:
            s_target, _ = sock.accept()
            send_file(s_target,user,file_name)
            # threading.Thread(target=traiter_client,
            # args=(sock_client,)).start()
        except KeyboardInterrupt:
            break

    # send_thread = threading.Thread(target=send_file, args=(s_target, user, file_name))
    # send_thread.start()
    # send_thread.join()
    # sys.exit(0)
    

def prepare_share_file(sock, m_formatted):
    global file_queue
    file_name = m_formatted[2]
    file_stats = os.stat(file_name)
    
    #A Socket for each file to send
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(("", int(m_formatted[3])))
    # s.listen(4)
    # Dict of all files to send
    if m_formatted[1] in file_queue.keys():
        file_queue[m_formatted[1]].extend([file_name])
    else:
        file_queue[m_formatted[1]] = [file_name]

    # A thread for each file we send
    threading.Thread(target=accept_file_from_srv, args=(sock, m_formatted[1], file_name)).start()
    for t in threading.enumerate():
        if t != threading.main_thread(): 
            t.join
    # To attach it to the command
    return f" {file_stats.st_size}"


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
        if u == user and file == f[0]:
            size = f[1]
            adr_ip = f[2]
            port = f[3]
            s.connect((str(adr_ip), int(port)))
            reception_thread = threading.Thread(target=wait_for_file_arrival, args=(s, size, user, file))
            reception_thread.start()
            reception_thread.join()

def wait_for_file_arrival(sock, size, user, file):
    progress = tqdm.tqdm(range(size), f"Receiving {user}", unit="B", unit_scale=True, unit_divisor=1024)
    with sock:
        with open(file, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = sock.recv(4096)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
        progress.update(len(bytes_read))
    sys.exit(0)

# Create a socket object
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((adresse, int(port)))
# Start threads for receiving and sending data
recv_thread = threading.Thread(target=listen_server_cmd, args=(s,))
send_thread = threading.Thread(target=talk_to_server, args=(s,))
recv_thread.start()
send_thread.start()


# Wait for threads to finish
recv_thread.join()
send_thread.join()
sys.exit(0)
