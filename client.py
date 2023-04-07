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
    "415": "Already afk",
    "416": "Alredy btk",
    "421": "Private channel does not exist",
    "425": "Username already taken",
    "500": "Internal server error",
}

#Partie stockage utilisateur
username = ""
lastCommand = ""

#Methodes
def listen_server_cmd(sock):
    with sock:
        while True:
            reponse = sock.recv(256)
            reponse = reponse.decode()
            reponse.split("|", 1)
            print(reponse)
            if reponse[0] != "200" :
                print("Erreur :" + reponse)
            else:
            #Traitement des messages constants du serveur
                match lastCommand:
                    case "help":
                        print(reponse[1])
                    case "signup":
                        username = lastCommand.split(" ", 1)
                        username = username[1]
                    case "msg":
                        print(reponses_possibles[reponse[0]])
                    case "msgpv":
                        print(reponses_possibles[reponse[0]])
                    case "exit":
                        print(reponses_possibles[reponse[0]])
                    case "afk":
                        print(reponses_possibles[reponse[0]])
                    case "btk":
                        print(reponses_possibles[reponse[0]])
                    case "users":
                        print(reponse[1])
                    case "rename":
                        username = lastCommand.split(" ", 1)
                        username = username[1]
                    case "pingFromSrv":
                        print(f"reponse[1] has pinged you")
                    case "channel":
                        pass
                    case "acceptchannel":
                        pass
                    case "declinechannel":
                        pass
                    case "sharefile":
                        pass
                    case "acceptfile":
                        pass
                    case "declinefile":
                        pass
                    case other:
                        pass

def talk_to_server(sock):
    with sock:
        while True:
            lastCommand = input("Pour commencer entrer la commande signup\n")
            if lastCommand.upper() == "QUIT":
                break
            print(lastCommand)
            sock.sendall(lastCommand.encode())
    

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