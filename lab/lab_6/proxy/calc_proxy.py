import socket
import _thread as thread


def recv_all(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def handle_client(client_socket, client_addr):
    print("New client:", client_addr)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("localhost", 5555))

    while True:
        s = recv_all(client_socket, 12)
        if len(s) == 0:
            print("Connection closed by", client_addr)
            conn.close()
            return

        conn.sendall(s)
        resp = recv_all(conn, 4)
        if len(resp) == 0:
            print("Target connection closed")
            return

        client_socket.sendall(resp)

    print("Bye Client!")


# create sercver socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 8888))
s.listen(1)

while True:
    # accept client
    client_socket, client_addr = s.accept()

    # start new thread and handle client
    thread.start_new_thread(handle_client, (client_socket, client_addr))
