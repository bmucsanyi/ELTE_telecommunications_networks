import socket
import struct  # https://docs.python.org/3.7/library/struct.html
import threading


def get_values_from_calc_struct(s):
    return struct.unpack('ici', s)


def create_result_struct(r):
    return struct.pack('i', r)


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def handle_client(client_socket, client_addr):
    print("New client:", client_addr)
    while True:
        s = recvall(client_socket, 12)
        if len(s) == 0:
            print("Connection closed by", client_addr)
            print("Bye Client!")
            return

        p1, op, p2 = get_values_from_calc_struct(s)
        op = op.decode()
        print(p1, op, p2)
        if op == "+":
            client_socket.sendall(create_result_struct(p1 + p2))
        elif op == "-":
            client_socket.sendall(create_result_struct(p1 - p2))
        elif op == "*":
            client_socket.sendall(create_result_struct(p1 * p2))
        elif op == "/" and p2 != 0:
            client_socket.sendall(create_result_struct(p1 // p2))
        else:
            client_socket.sendall(create_result_struct(0))


def main():
    # create server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 5555))
    s.listen(1)
    # When multiple clients connect to the server, the server then holds the
    # incoming requests in a queue. The clients are arranged in the queue, and
    # the server processes their requests one by one as and when queue-member
    # proceeds. The nature of this kind of connection is called queued connection.
    # The backlog parameter of listen is the size of this queue.
    # If the queue is full, new connections are automatically declined.

    while True:
        # accept client
        client_socket, client_addr = s.accept()

        # start new thread and handle client
        thread = threading.Thread(target=handle_client,
                                  args=(client_socket, client_addr))
        thread.start()


if __name__ == "__main__":
    main()
