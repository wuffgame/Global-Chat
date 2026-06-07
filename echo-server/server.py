import socket
import threading

ids = [1, 2, 3, 4, 5]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
server.listen(5)

def cclient(client, addr):
    cid = ids[0]
    ids.remove(cid)
    if client.recv(1024).decode() == "B0.1":
        print(f"Connected with {addr}, using id {cid}")
        client.send("True".encode())
    else:
        print("Error while connecting!!!")

    try:
        while True:
            data = client.recv(1024)
            if not data:
                print(f"Disconnected with {addr}")
                ids.insert(cid - 1, cid)
                break
            print(f"Message from client with id {cid}: ", data.decode())
            client.send(data)
    except ConnectionResetError:
        print(f"Disconnected with {addr}")
        ids.insert(cid - 1, cid)
        client.close()
    finally:
        client.close()

while True:
    client, addr = server.accept()
    threading.Thread(target=cclient, args=(client, addr), daemon=True).start()