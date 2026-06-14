import socket
import threading
import time
import os

os.environ["PROMPT_TOOLKIT_NO_CPR"] = "1"

from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

print("IMPORTANT!!! Chat doesn't have a login system, so anyone can use any username they want, including yours or your friend's when you're inactive. Please don't trust what others say until you verify it through Slack or Discord. I plan to implement such a system someday, but it's currently unavailable!!!")
username = input("Type your username: ")

if client.recv(1024).decode() == "You are banned from this server!!!":
    print("You are banned from this server!!!")

client.send("B0.5".encode())
if client.recv(1024).decode() == "True":
    print("Connected to server")
else:
    print("Old version of client")
    os._exit(0)
client.send(username.encode())

m = client.recv(1024).decode()
if m == "This username is on chat!!! Please choose another!!!":
    print(m)
    client.close()
    os._exit(0)

def receive():
    while True:
        try:
            print(client.recv(1024).decode())
        except OSError:
            print("Disconnected with server!!!")
            client.close()
            os._exit(0)

def send():
    while True:
        with patch_stdout():
            message = prompt("> ")
            client.send(message.encode())


threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=send, daemon=True).start()

try:
    while True:
        time.sleep(1)
finally:
    os._exit(0)