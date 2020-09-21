import socket

server_addr = ('192.168.0.111', 10000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(server_addr)

    print("Send message:")
    message = input()
    client.sendall(message.encode())

    data = client.recv(16).decode()
    print("Received:", data)