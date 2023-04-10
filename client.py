import socket
import sys
import threading

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
lastCommand = ""
liste_msg = []
liste_msg_pv = []

#Methodes
def listen_server_cmd(sock):
    global lastCommand, username, liste_msg, reponses_possibles, commands_from_srv, liste_msg_pv
    with sock:
        while True:
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
                if r_formatted[0] not in commands_from_srv:
                    command = lastCommand.split(' ')
                    match command[0]:
                        case "help":
                            print(r_formatted[1])
                        case "signup":
                            username = lastCommand.split(" ", 1)
                            username = username[1]
                            print("You are now connected")
                        case "msg":
                            print("Message envoyé")
                            # liste_msg += f"{r_formatted[1]} : {r_formatted[2]}\n"
                            # for mess in liste_msg:
                            #     print(mess)
                        case "msgpv":
                            print("Message privé envoyé")
                            # liste_msg_pv += f"{r_formatted[1]} : {r_formatted[2]}\n"
                            # for mess in liste_msg_pv:
                            #     print(f"discussion avec {r_formatted[1]}")
                            #     print(mess)
                        case "exit":
                            print("You are now offline")
                        case "afk":
                            print("You are now afk")
                        case "btk":
                            print("You are now btk")
                        case "users":
                            print(r_formatted[1])
                        case "rename":
                            print("You have been renamed")
                            # username = lastCommand.split(" ", 1)
                            # username = username[1]
                        case "ping":
                            print("You pinged someone")
                        case "channel":
                            print("Your request channel has been sent")
                        case "acceptchannel":
                            print("Your request channel has been accepted")
                        case "declinechannel":
                            print("Your request channel has been declined")
                        case "sharefile":
                            pass
                        case "acceptfile":
                            pass
                        case "declinefile":
                            pass
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
                            # liste_msg += f"{r_formatted[1]} : {r_formatted[2]}\n"
                            # for mess in liste_msg:
                            #     print(mess)
                        case "exitedFromSrv":
                            print(f"{r_formatted[1]} has exited the server")
                        case "afkFromSrv":
                            print(f"{r_formatted[1]} is now afk")
                        case "btkFromSrv":
                            print(f"{r_formatted[1]} is back to the party !")
                        case "usersFromSrv":
                            pass
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
                        case "acceptedfileFromSrv":
                            print(f"{r_formatted[1]} has accepted to receive your file")
                        case "declinedfileFromSrv":
                            print(f"{r_formatted[1]} doesn't want files from you D: ")


def talk_to_server(sock):
    global lastCommand, username, liste_msg
    with sock:
        while True:
            cmd = input("$ ")
            if cmd.upper() == "QUIT":
                break
            lastCommand = cmd
            sock.sendall(cmd.encode())
    

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
