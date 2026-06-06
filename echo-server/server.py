import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
server.listen(1)
client, addr = server.accept()

if client.recv(1024).decode() == "123":
    print(f"Connected with {addr}")
    client.send("True".encode())
else:
    print("Error while connecting!!!")
    exit(0)

while True:
    data = client.recv(1024)
    if not data:
        exit(0)
    print("Message from client: ", data.decode())
    client.send(data)