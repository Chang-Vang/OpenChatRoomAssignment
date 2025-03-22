import threading
import sys
from socket import *
import json
import os

clients = {}
lock = threading.Lock()
USERS_FILE = "../users.json"

# --------------------------------------------------------------------
# Load user credentials from file
def load_users():
    """Load user credentials from the file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

# --------------------------------------------------------------------
# Save user credentials to file
def save_users(users):
    """Save user credentials to the file."""
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

# --------------------------------------------------------------------
# Handling Client Connection
def handle_client(client_sock, addr):
    """Thread to handle communication with a connected client."""
    username = None
    print(f"Connection established with {addr}")
    try:
        while True:
            # Receive message from client
            message = client_sock.recv(1024).decode('utf-8')
            if not message:
                print(f"Client {addr} disconnected.")
                break

            data = json.loads(message)
            if data['command'] == 'login':
                username = data['username']
                password = data['password']

                users = load_users()
                if username in users:
                    # Existing user: verify password
                    if users[username] == password:
                        client_sock.send(json.dumps({'type': 'login', 'status': 'success'}).encode('utf-8'))
                        with lock:
                            clients[username] = client_sock
                        broadcast_user_list()
                    else:
                        client_sock.send(json.dumps({'type': 'login', 'status': 'failure', 'message': 'Incorrect password'}).encode('utf-8'))
                else:
                    # New user: register and save credentials
                    users[username] = password
                    save_users(users)
                    client_sock.send(json.dumps({'type': 'login', 'status': 'success'}).encode('utf-8'))
                    with lock:
                        clients[username] = client_sock
                    broadcast_user_list()

            elif data['command'] == 'PM':
                broadcast_message(username, data['message'])
            elif data['command'] == 'DM':
                send_dm(username, data['target'], data['message'])
            elif data['command'] == 'EX':
                break

    except ConnectionError:
        print(f"Connection error with {addr}.")

    finally:
        if username:
            with lock:
                del clients[username]
            broadcast_user_list()
        print(f"Closing connection to {addr}")
        client_sock.close()

# --------------------------------------------------------------------
# Broadcasting Messages
def broadcast_message(sender, message):
    with lock:
        for user, sock in clients.items():
            if user != sender:
                sock.send(json.dumps({'type': 'broadcast',
                                      'from': sender,
                                      'message': message}).encode('utf-8'))

# --------------------------------------------------------------------
# Direct Messaging DM
def send_dm(sender, target, message):
    with lock:
        if target in clients:
            clients[target].send(json.dumps({'type': 'direct',
                                             'from': sender,
                                             'message': message}).encode('utf-8'))

# --------------------------------------------------------------------
# Broadcasting User List
def broadcast_user_list():
    with lock:
        user_list = list(clients.keys())
        for user, sock in clients.items():
            sock.send(json.dumps({'type': 'user_list',
                                  'users': user_list}).encode('utf-8'))

# --------------------------------------------------------------------
# Running Server
def run_server(host_address, server_port):
    """Main function to run the server."""
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind((host_address, server_port))
    server_sock.listen(100)
    print(f"Server running on {host_address}:{server_port}")

    while True:
        # Accept client connection
        client_sock, addr = server_sock.accept()

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        client_thread.start()

        print(f"Started thread for {addr}")

# --------------------------------------------------------------------
# Main Function
if __name__ == '__main__':
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <host_ip> <server_port>")
        sys.exit(1)

    # Get the host IP address from the first argument
    host_address = sys.argv[1]

    # Get the port number from the second argument
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("Port number must be an integer.")
        sys.exit(1)

    # Validate the port number
    if not (1024 <= server_port <= 65535):
        print("Port number must be between 1024 and 65535.")
        sys.exit(1)

    # Start the server
    run_server(host_address, server_port)