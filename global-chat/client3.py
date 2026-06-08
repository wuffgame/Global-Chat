import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

username = input("Type your username: ")

client.send("B0.2".encode())
if client.recv(1024).decode() == "True":
    print("Connected to server")
else:
    print("Old version of client")
    exit(0)

def receive():
    while True:
        try:
            print(client.recv(1024).decode())
        except OSError:
            print("Disconnected with server!!!")
            exit(0)


threading.Thread(target=receive, daemon=True).start()

while True:
    message = input("> ")
    message = f"{username}: {message}"
    client.send(message.encode())