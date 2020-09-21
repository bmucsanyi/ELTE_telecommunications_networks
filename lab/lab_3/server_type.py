import socket
# https://www.tutorialspoint.com/unix_sockets/what_is_socket.htm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = (socket.gethostname(), 10000)

server.bind(server_addr)
server.listen(1)
server.settimeout(1)

while True:
    try:
        client, client_addr = server.accept()

        print("Connected:", client_addr)

        data = client.recv(16)
        print("Received:", data.decode())

        client.sendall("Received!".encode())

        client.close()
    except socket.timeout as p:
        pass
    except socket.error as e:
        print(e)