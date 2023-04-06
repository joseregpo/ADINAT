import threading
import socket

def handle_client(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            print(data.decode())

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('localhost', 8080))
    s.listen()

    while True:
        # Wait for a connection
        conn, addr = s.accept()

        # Start a new thread to handle the connection
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()