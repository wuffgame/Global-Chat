import socket
import threading

clients = []
lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(5)

def broadcast(message):
    with lock:
        for client in clients:
            try:
                client.send(message)
            except:
                clients.remove(client)

def cclient(client, addr):
    if client.recv(1024).decode() == "B0.2":
        print(f"Connected with {addr}")
        client.send("True".encode())
    else:
        print("Too old client version!!!")
        client.send("False".encode())
        client.close()

    clients.append(client)

    try:
        while True:
            data = client.recv(1024)
            if not data:
                print(f"Disconnected with {addr}")
                break
            message = data
            print(data.decode())
            broadcast(message)

    except ConnectionResetError:
        print(f"Disconnected with {addr}")
        with lock:
            if client in clients:
                clients.remove(client)
        client.close()
    finally:
        with lock:
            if client in clients:
                clients.remove(client)
        client.close()

while True:
    client, addr = server.accept()
    threading.Thread(target=cclient, args=(client, addr), daemon=True).start()