import socket

server_addr = ('192.168.0.111', 10000)  # localhost ---DNS---> 127.0.0.1
# We want to connect to this host (not case sensitive), to this exact port.
# If we connect to a wrong port,
# we get a ConnectionRefusedError.

# If we type '192.168.0.111'
# (socket.gethostbyname(socket.gethostname()) on server),
# we also get a ConnectionRefusedError,
# as we only opened the socket to the localhost!
# These two are not the same!
# With '192.168.0.111' opened on the server,
# we can reach the server from the whole LAN.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:  # like a file descriptor
    client.connect(server_addr)

    print("Send hello")
    client.sendall("Hello szerver".encode())

    data = client.recv(16).decode()  # default: utf-8
    print("Kaptam:", data)