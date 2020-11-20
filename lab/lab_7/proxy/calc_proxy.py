import socket
import _thread as thread


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def handle_client(client_socket, client_addr):
    print("New client:", client_addr)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 5555))  # connect to server

    while True:
        s = recvall(client_socket, 12)
        if len(s) == 0:
            print("Connection closed by", client_addr)
            conn.close()
            return

        conn.sendall(s)
        resp = recvall(conn, 4)
        if len(resp) == 0:
            print("Target connection closed")
            return

        client_socket.sendall(resp)


# create sercver socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# When retrieving a socket option, or setting it, you specify the option name as
# well as the level. When level = SOL_SOCKET, the item will be searched for in
# the socket itself.
# 1 means True.
s.bind(("localhost", 8888))
s.listen(1)  # the number of unaccepted connections that the system will allow before refusing new connections

while True:
    # accept client
    client_socket, client_addr = s.accept()

    # start new thread and handle client
    thread.start_new_thread(handle_client, (client_socket, client_addr))
