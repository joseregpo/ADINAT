import socket
import sys
import threading

def traiter_client(sock_fille):
    while True:
        mess = sock_fille.recv(256)
        
        match mess.decode():
            case "help":
                sock_fille.sendall(mess.upper())
            case "login":
                sock_fille.sendall(mess.upper())
            case "msg":
                sock_fille.sendall(mess.upper())
            case "msgpv":
                sock_fille.sendall(mess.upper())
            case "exit":
                sock_fille.sendall(mess.upper())
            case "afk":
                sock_fille.sendall(mess.upper())
            case "btk":
                sock_fille.sendall(mess.upper())
            case "users":
                sock_fille.sendall(mess.upper())
            case "rename":
                sock_fille.sendall(mess.upper())
            case "ping":
                sock_fille.sendall(mess.upper())
            case "channel":
                sock_fille.sendall(mess.upper())
            case "acceptchannel":
                sock_fille.sendall(mess.upper())
            case "declinechannel":
                sock_fille.sendall(mess.upper())
            case "sharefile":
                sock_fille.sendall(mess.upper())
            case "acceptfile":
                sock_fille.sendall(mess.upper())
            case "declinefile":
                sock_fille.sendall(mess.upper())
            case other:
                sock_fille.sendall("Unknown command".encode())

with socket.socket() as sock_locale:
    sock_locale.bind(("", int(sys.argv[1])))
    sock_locale.listen(4)
    
    while True:
        try:
            sock_client, adr_client = sock_locale.accept()
            threading.Thread(target=traiter_client,
            args=(sock_client,)).start()
        except KeyboardInterrupt:
            break

print("Bye")



for t in threading.enumerate():
    if t != threading.main_thread(): t.join
    
sys.exit(0)
