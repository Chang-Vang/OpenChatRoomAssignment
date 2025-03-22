# Online Chat Room Application
A simple chat room application that supports public messages (PM), direct messages (DM), and user authentication. The server handles multiple clients, and user credentials are stored in a file.

---

## How to Run

### 1. Start the Server
Open a terminal, navigate to the folder that holds the python files and run:
```
python serverSide.py <host_ip> <server_port>
```
Example:
```
python serverSide.py 0.0.0.0 5000
```

---

### 2. Start the Client
Open another terminal, navigate to the folder that holds the python files and run:
```
python clientSide.py <server_ip> <server_port>
```
Example:
```
python clientSide.py localhost 5000
```

---

### 3. Log In
- Enter a username and password when prompted.
- If the username is new, it will be registered.
- If the username exists, the password will be verified.

---

### 4. Use the Chat Room
- **Public Message (PM)**: Send a message to all users.
  ```
  Choose operation (PM, DM, EX): PM
  Enter public message: Hello, everyone!
  ```
- **Direct Message (DM)**: Send a message to a specific user.
  ```
  Choose operation (PM, DM, EX): DM
  Enter target username: Tom
  Enter direct message: Hey Tom!
  ```
- **Exit (EX)**: Disconnect from the chat room.
  ```
  Choose operation (PM, DM, EX): EX
  Exiting...
  ```

---

## Example

### Terminal 1 (Server)
```bash
python serverSide.py 0.0.0.0 5000
Server running on 0.0.0.0:5000
```

### Terminal 2 (Client 1)
```bash
python clientSide.py localhost 5000
Enter username: Jayce
Enter password: Jayce
Choose operation (PM, DM, EX): PM
Enter public message: Hello, everyone!
```

### Terminal 3 (Client 2)
```bash
python clientSide.py localhost 5000
Enter username: Harry
Enter password: Harry
Choose operation (PM, DM, EX): DM
Enter target username: Jayce
Enter direct message: Hello Jayce
```

---

## Notes
- **Credentials**: Stored in `users.json` on the server.
- **Multiple Clients**: Run multiple clients to simulate multiple users.
- **Exit**: Use `EX` to disconnect.

---
