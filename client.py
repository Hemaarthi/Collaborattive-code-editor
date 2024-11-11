import socket
import threading

# Server details
HOST = '127.0.0.1'
PORT = 12345

def receive_data(client_socket):
    while True:
        try:
            # Receive data from the server
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"\nReceived: {data}")
        except ConnectionResetError:
            break

def send_data(client_socket):
    while True:
        # Read user input
        message = input("Enter code: ")
        try:
            # Send user input to server
            client_socket.send(message.encode('utf-8'))
        except BrokenPipeError:
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connected to the server.")

    # Start threads for sending and receiving data
    threading.Thread(target=receive_data, args=(client_socket,)).start()
    send_data(client_socket)

if __name__ == "__main__":
    start_client()