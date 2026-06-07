import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

client.send("B0.1".encode())
if client.recv(1024).decode() == "True":
    print("Connected with server!!!")
else:
    print("Error while connecting!!!")
    exit(0)

while True:
    message = input("Type message for server: ")
    client.send(message.encode())
    data = client.recv(1024).decode()
    print("Message from server: ", data)