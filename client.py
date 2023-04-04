import socket
import sys

adresse, port = sys.argv[1].split(":")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_locale:
    sock_locale.connect((adresse, int(port)))
    while True:
        commande = input("Pour commencer entrer la commande login\n")
        if commande.upper() == "QUIT":
            break
        sock_locale.send(commande.encode())
        reponse = sock_locale.recv(256)
        
        match reponse.decode():
            case "200":
                print("Success")
            case "400":
                print("The command doesn’t exist probably due to a typing error")
            case "401":
                print("Message error")
            case "402":
                print("Username does not exist")
            case "403":
                print("Wrong numbers of parameters")
            case "404":
                print("Private channel already exists")
            case "405":
                print("File name does not exist")
            case "415":
                print("Already afk")
            case "416":
                print("Alredy btk")
            case "421":
                print("Private channel does not exist")
            case "425":
                print("Username already taken")
            case "500":
                print("Internal server error")

            
