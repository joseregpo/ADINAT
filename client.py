import socket
import sys

adresse, port = sys.argv[1].split(":")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_locale:
    sock_locale.connect((adresse, int(port)))
    while True:
        commande = input("Informez-vous des commandes avec help et lancez en une\n")
        if commande.upper() == "QUIT":
            break
        sock_locale.send(commande.encode())
        reponse = sock_locale.recv(256)
        print(reponse.decode())
