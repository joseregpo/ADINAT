import socket
import sys

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_locale:
    sock_locale.connect((adresse, int(port)))
    while True:
        commande = input("Pour commencer entrer la commande signup\n")
        if commande.upper() == "QUIT":
            break
        sock_locale.send(commande.encode())
        reponse = sock_locale.recv(256)
        reponse = reponse.decode()
        reponse.split("|", 1)
        if reponse[0] != "200" :
            print(reponses_possibles[reponse])
        else:

            #Traitement des messages constants du serveur
            match commande:
                case "help":
                    print(reponse[1])
                case "signup":
                    username = commande.split(" ", 1)
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
                    username = commande.split(" ", 1)
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

