import random
import socket
import struct


def pack(num_list, money):
    return struct.pack('5iQ', *num_list, money)


def unpack(resp):
    return struct.unpack('5iQ', resp)


def pack_history(winner_numbers, tips, money):
    return struct.pack('10iQ', *winner_numbers, *tips, money)


def handle_client(data):
    highest_price = struct.unpack('i', data)
    print('New highest price:', highest_price)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', 22222))

        while True:
            data, _ = server.recvfrom(struct.calcsize('i'))
            # nem kell timeout, hiszen egy szerver
            handle_client(data)


if __name__ == "__main__":
    main()