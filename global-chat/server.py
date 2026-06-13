import socket
import threading
import time
import json
import os
from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

clients = []
lock = threading.Lock()
nicks = {}
last_msg_time = {}
bans = []
BansFile = "bans.json"
history = []
cooldown_time = 2.0
disconnect = []

if os.path.exists(BansFile):
    with open("bans.json", "r") as file:
        bans = json.load(file)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 12345))
server.listen(1)


def broadcast(message):
    with lock:
        if len(history) >= 10:
            history.pop(0)
        try:
            decoded_msg = message.decode()
        except:
            decoded_msg = str(message)
        messages = f"\n{decoded_msg}"
        history.append(messages.encode())
        for cl in list(clients):
            try:
                cl.send(message)
            except:
                if cl in clients:
                    clients.remove(cl)

def cclient(client, addr):
    try:
        client_ip = client.getpeername()[0]
        if client_ip in bans:
            client.send("You are banned from this server!!!".encode())
            client.close()
        client.send("True".encode())
        version = client.recv(1024).decode()

        if version != "B0.5":
            print(f"Rejected {addr}")
            client.send("False".encode())
            client.close()
            return

        client.send("True".encode())
        nick = client.recv(1024).decode()
        with lock:
            if nick not in nicks.values():
                client.send("True".encode())
                nicks[client] = nick
                last_msg_time[client] = 0.0
            else:
                client.send("This username is on chat!!! Please choose another!!!".encode())
                return
        print(f"Connected with {addr}")
        broadcast(f"SYSTEM: {nicks[client]} joined the chat".encode())

        with lock:
            clients.append(client)

        for i in history:
            client.send(i)

        while True:
            if client in disconnect:
                break
            try:
                data = client.recv(1024)
                if not data:
                    break
            except:
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
            user_nick = nicks.get(client, "Unknown")
            if client in clients:
                clients.remove(client)
            if client in nicks:
                del nicks[client]
            if client in last_msg_time:
                del last_msg_time[client]
            if client in disconnect:
                msg = f"SYSTEM: {user_nick} has been kicked/banned from the chat"
                disconnect.remove(client)
            else:
                msg = f"SYSTEM: {user_nick} leave the chat"
        broadcast(msg.encode())
        try:
            client.close()
        except:
            pass
        print(f"Disconnected {user_nick}")

def inputs():
    while True:
        with patch_stdout():
            command = prompt()
            command_parts = command.split(maxsplit=1)
            if command_parts[0] == "ban":
                if command_parts[1] in nicks.values():
                    client_id = [k for k, v in nicks.items() if v == command_parts[1]][0]
                    client_ip = client_id.getpeername()[0]
                    bans.append(client_ip)
                    print(f"Banned {command_parts[1]}, with ip {client_ip}")
                    disconnect.append(client_id)
                    client_id.close()
                    with open(BansFile, "w") as file:
                        json.dump(bans, file, indent=4)
                else:
                    print("This user is not on chat!!!")
            if command_parts[0] == "unban":
                if command_parts[1] in bans:
                    bans.remove(command_parts[1])
                    with open(BansFile, "w") as file:
                        json.dump(bans, file, indent=4)
                    print(f"Unbanned {command_parts[1]}")
                else:
                    print("This user is not banned!!!")
            if command_parts[0] == "ban-list":
                print(bans)
            if command_parts[0] == "kick":
                if command_parts[1] in nicks.values():
                    client_id = [k for k, v in nicks.items() if v == command_parts[1]][0]
                    print(f"{command_parts[1]} has been kicked")
                    disconnect.append(client_id)
                    client_id.close()
            if command_parts[0] == "list":
                n = []
                for i in nicks.values():
                    n.append(i)
                print(f"Users on chat: {n}")
            if command_parts[0] == "say":
                if command_parts[1]:
                    broadcast(f"SYSTEM: {command_parts[1]}".encode())
                    print(f"SYSTEM: {command_parts[1]}")

            if command_parts[0] == "help":
                print("# ban username - ban user ip")
                print("# unban ip - unban ip")
                print("# ban-list - show banned ip")
                print("# kick username - kick user from chat")
                print("# list - show users on chat")
                print("# say message - send message on chat")
                print("# help - show list of commands")

threading.Thread(target=inputs, daemon=True).start()
while True:
    client, addr = server.accept()
    threading.Thread(target=cclient, args=(client, addr), daemon=True).start()