import socket
import sys
import threading

def traiter_client(sock_fille):
    while True:
        mess = sock_fille.recv(256)
        
        match mess.decode():
            case "help":
                print("je suis la")
                help(mess, sock_fille)
            case "login":
                login(mess, sock_fille)
            case "msg":
                msg(mess, sock_fille)
            case "msgpv":
                msgpv(mess, sock_fille)
            case "exit":
                exit(mess, sock_fille)
            case "afk":
                afk(mess, sock_fille)
            case "btk":
                btk(mess, sock_fille)
            case "users":
                users(mess, sock_fille)
            case "rename":
                rename(mess, sock_fille)
            case "ping":
                ping(mess, sock_fille)
            case "channel":
                channel(mess, sock_fille)
            case "acceptchannel":
                acceptchannel(mess, sock_fille)
            case "declinechannel":
                declinechannel(mess, sock_fille)
            case "sharefile":
                sharefile(mess, sock_fille)
            case "acceptfile":
                acceptfile(mess, sock_fille)
            case "declinefile":
                declinefile(mess, sock_fille)
            case other:
                sock_fille.sendall("Unknown command".encode())

def help(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def login(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def msg(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def msgpv(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def exit(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def afk(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def btk(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def users(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def rename(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def ping(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def channel(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def acceptchannel(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def declinechannel(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def sharefile(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def acceptfile(mess, sock_fille):
    sock_fille.sendall(mess.upper())

def declinefile(mess, sock_fille):
    sock_fille.sendall(mess.upper())


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
