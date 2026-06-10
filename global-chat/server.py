import socket
import threading
import time

clients = []
lock = threading.Lock()
nicks = {}
last_msg_time = {}

cooldown_time = 2.0

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
    try:
        version = client.recv(1024).decode()

        if version != "B0.3":
            print(f"Rejected {addr}")
            client.send("False".encode())
            client.close()
            return

        client.send("True".encode())
        nick = client.recv(1024).decode()
        with lock:
            if nick not in nicks.values():
                nicks[client] = nick
                last_msg_time[client] = 0.0
            else:
                client.send("This username is on chat!!! Please choose another!!!".encode())
                return
        print(f"Connected with {addr}")
        broadcast(f"SYSTEM: {nicks[client]} joined the chat".encode())

        with lock:
            clients.append(client)

        while True:
            data = client.recv(1024)
            if not data:
                break

            current_time = time.time()
            with lock:
                elapsed_time = current_time - last_msg_time.get(client, 0)
                if elapsed_time < cooldown_time:
                    remaining = round(cooldown_time - elapsed_time, 1)
                    client.send(f"SYSTEM: Don't spam!!! Wait {remaining}s".encode())
                    continue
                last_msg_time[client] = current_time

            data = data.decode()
            data = f"{nicks[client]}: {data}"
            print(data)
            data = data.encode()
            broadcast(data)

    except ConnectionResetError:
        pass

    finally:
        with lock:
            if client in clients:
                clients.remove(client)
            if client in nicks:
                del nicks[client]
            if client in last_msg_time:
                del last_msg_time[client]
        client.close()
        print(f"Disconnected {addr}")

while True:
    client, addr = server.accept()
    threading.Thread(target=cclient, args=(client, addr), daemon=True).start()