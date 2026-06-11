import socket
import threading
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

username = input("Type your username: ")

client.send("B0.3".encode())
if client.recv(1024).decode() == "True":
    print("Connected to server")
else:
    print("Old version of client")
    exit(0)
client.send(username.encode())

m = client.recv(1024).decode()
if m == "This username is on chat!!! Please choose another!!!":
    print(m)
    client.close()
    exit(0)

def receive():
    while True:
        try:
            print(client.recv(1024).decode())
        except OSError:
            print("Disconnected with server!!!")
            client.close()
            break


threading.Thread(target=receive, daemon=True).start()

while True:
    with patch_stdout():
        message = prompt("> ")
        client.send(message.encode())