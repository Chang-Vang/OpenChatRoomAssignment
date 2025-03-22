import threading
import sys
from socket import *
import json

# -------------------------------------------------------------------
# Receiving Messages
def receive_messages(sock):
    """Thread for receiving messages from the server."""
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                data = json.loads(message)
                if data['type'] == 'broadcast':
                    print(f"Broadcast from {data['from']}: {data['message']}")
                elif data['type'] == 'direct':
                    print(f"Direct Message from {data['from']}: {data['message']}")
                elif data['type'] == 'user_list':
                    print("Active users:", data['users'])
                elif data['type'] == 'login':
                    if data['status'] == 'failure':
                        print(data['message'])
                        sock.close()
                        sys.exit(1)
            else:
                print("Server connection lost.")
                break
        except ConnectionError:
            print("Connection error.")
            break

# -------------------------------------------------------------------
# Sending Messages
def send_messages(sock):
    """Thread for sending messages from user input to the server."""
    while True:
        action = input("Choose operation (PM, DM, EX): ").upper()
        if action == 'PM':
            message  = input("Enter public message: ")
            sock.send(json.dumps({'command': 'PM',
                                  'message': message}).encode('utf-8'))
        elif action == 'DM':
            target = input("Enter target username: ")
            message  = input("Enter direct message: ")
            sock.send(json.dumps({'command': 'DM',
                                  'target': target,
                                  'message': message}).encode('utf-8'))
        elif action == 'EX':
            sock.send(json.dumps({'command': 'EX'}).encode('utf-8'))
            print("Exiting...")
            sock.close()
            break
        else:
            print("Invalid operation. Choose PM, DM, or EX.")

# -------------------------------------------------------------------
# Main Client Function
def run_client(host_address, server_port):
    """Main function to run the client."""
    client_sock = socket(AF_INET, SOCK_STREAM)
    try:
        client_sock.connect((host_address, server_port))
    except ConnectionRefusedError:
        print("Could not connect to the server.")
        return

    # Log in
    username = input("Enter username: ")
    password = input("Enter password: ")
    client_sock.send(json.dumps({'command': 'login',
                                 'username': username,
                                 'password': password}).encode('utf-8'))

    # Wait for login response
    response = client_sock.recv(1024).decode('utf-8')
    data = json.loads(response)
    if data['type'] == 'login' and data['status'] == 'failure':
        print(data['message'])
        client_sock.close()
        return

    # Create two threads: one for receiving messages, one for sending them
    receive_thread = threading.Thread(target=receive_messages, args=(client_sock,))
    send_thread = threading.Thread(target=send_messages, args=(client_sock,))

    # Start both threads
    receive_thread.start()
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    print("Client connection closed.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        # 5000 is just a port example. Port number has to be between 1024 and 65535
        # You must use the same port number that the server is open on.
        print('Terminal line example: Python clientSide.py localhost 5000')
        sys.exit(1)

    host_address = sys.argv[1]
    server_port = int(sys.argv[2])
    run_client(host_address, server_port)