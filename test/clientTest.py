import threading
import socket

def recv_data(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print('Received:', data.decode())

def send_data(sock):
    while True:
        message = input('Enter message: ')
        sock.sendall(message.encode())

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 8080))

    # Start threads for receiving and sending data
    recv_thread = threading.Thread(target=recv_data, args=(s,))
    send_thread = threading.Thread(target=send_data, args=(s,))
    recv_thread.start()
    send_thread.start()

    # Wait for threads to finish
    recv_thread.join()
    send_thread.join()