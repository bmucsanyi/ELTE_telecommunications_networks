import random
import socket
import struct


def pack(extra_num):
    return struct.pack('i', extra_num)


def handle_client(data, addr, sock):
    print("New client:", addr)

    if data == b'help':
        extra_num = random.randint(1, 100)
        resp = pack(extra_num)
        sock.sendto(resp, addr)
    else:
        print('unknown request:', data.decode())


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 22222))

        while True:
            data, addr = server.recvfrom(4096)
            handle_client(data, addr, server)


if __name__ == "__main__":
    main()