import socket
import struct  # https://docs.python.org/3.7/library/struct.html
import _thread


def get_values_from_calc_struct(s):
    return struct.unpack('ici', s)


def create_result_struct(r):
    return struct.pack('i', r)


def recv_all(sock, length):
    # waitall bloks recv until the EXACT byte count is reached
    return sock.recv(length, socket.MSG_WAITALL)


def handle_client(client_socket, client_addr):
    print("New client:", client_addr)
    while True:
        s = recv_all(client_socket, 12)
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
        elif op == "/":
            client_socket.sendall(create_result_struct(p1 // p2))


def main():
    # create sercver socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 5555))
    s.listen(1)

    while True:
        # accept client
        client_socket, client_addr = s.accept()  # can't Ctrl + C out on Windows!
        # have to Ctrl + C, then start the client to get out of the blocking phase

        # start new thread and handle client
        _thread.start_new_thread(handle_client, (client_socket, client_addr))


if __name__ == "__main__":
    main()