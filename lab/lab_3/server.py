import socket
# https://www.tutorialspoint.com/unix_sockets/what_is_socket.htm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_addr[0] is the host name
# server_addr[1] is our port number to which we wish to bind the host
# https://whatismyipaddress.com/localhost
server_addr = (socket.gethostname(), 10000)

server.bind(server_addr)
server.listen(1)
server.settimeout(1)  # másodpercenként lője ki a revc-t és accept-et
# windows-on nem lehet kilőni a recv-t és accept-et CTRL + C-vel

while True:
    try:
        client, client_addr = server.accept()
        # we need a separate socket ("file descriptor") for each client,
        # as there can be many clients connecting to us

        print("Csatlakozott:", client_addr)

        data = client.recv(16)  # we can get data from each socket...
        print("Kaptam:", data)
        print("Kaptam dekódolva:", data.decode())

        client.sendall("Hello kliens".encode())  # and we can send data to each socket...
        # "send" only sends the message to the network card,
        # whereas sendall asks the network card to send the message, too

        client.close()
    except socket.timeout as p:
        # print(p)
        pass
    except socket.error as e:
        print(e)