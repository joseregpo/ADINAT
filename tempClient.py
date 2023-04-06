import socket
import sys
import threading 

def send_tosrv(sock):
    # while True:
    #     message = input('Enter message: ')
    #     sock.sendall(message.encode())
    while True:
        commande = input("Pour commencer entrer la commande login\n")
        if commande.upper() == "QUIT":
            break
        sock.send(commande.encode())

def listen_to_srv(sock):
    while True:
        reponse = sock.recv(256)
        
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

adresse, port = sys.argv[1].split(":")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_locale:
    sock_locale.connect((adresse, int(port)))
    threading.Thread(target=send_tosrv, args=(sock_locale,)).start()
    threading.Thread(target=listen_to_srv, args=(sock_locale,)).start()
    # send_tosrv(sock_locale)
    # listen_to_srv(sock_locale)

for t in threading.enumerate():
    if t != threading.main_thread(): 
        t.join

sys.exit(0)