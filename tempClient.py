import socket
import sys
import threading 

def send_to_srv(sock):
    # while True:
    #     message = input('Enter message: ')
    #     sock.sendall(message.encode())
    print(sock)
    while True:
        commande = input("Pour commencer entrer la commande login\n")
        print(sock)
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

sock_locale = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock_locale.connect((adresse, int(port)))
t_read = threading.Thread(target=listen_to_srv, args=(sock_locale,)).start()
t = threading.Thread(target=send_to_srv, args=(sock_locale,)).start()

for t in threading.enumerate():
    if t != threading.main_thread(): 
        t.join

# sock_locale.close()
    # send_tosrv(sock_locale)
    # listen_to_srv(sock_locale)

