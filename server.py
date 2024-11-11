import socket
import threading

# Server details
HOST = '127.0.0.1'
PORT = 12345

# List to hold all connected clients
clients = []

def handle_client(client_socket, addr):
    print(f"Connection from {addr} established.")
    while True:
        try:
            # Receive data from client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received from {addr}: {data}")
            broadcast(data, client_socket)
        except ConnectionResetError:
            break
    print(f"Connection from {addr} closed.")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    # Send the received message to all clients except the sender
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except BrokenPipeError:
                client.close()
                clients.remove(client)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        # Start a new thread for each client
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()