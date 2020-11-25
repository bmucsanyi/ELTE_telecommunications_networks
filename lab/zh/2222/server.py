import random
import socket
import struct


def pack(num_list, money):
    return struct.pack('5iQ', *num_list, money)


def unpack(resp):
    return struct.unpack('5iQ', resp)


def pack_history(winner_numbers, tips, money):
    return struct.pack('10iQ', winner_numbers, tips, money)


def handle_client(data, addr, sock, winner_numbers, history):
    print("New client:", addr)

    # Client
    data = unpack(data)
    money = data[-1]
    tips = [num for num in data[:-1]]
    
    good_tips = len(set(tips) ^ set(winner_numbers))

    num_list = winner_numbers
    money *= good_tips
    data = pack(num_list, money)

    sock.sendto(data, addr)

    # History server
    history_data = pack_history(winner_numbers, tips, money)
    history.sendall(history_data)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 22222))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as history:
            history.connect(('localhost', 11111))  # 11111 is the history server

            winner_numbers = [random.randint(1, 20) for _ in range(5)]
            while True:
                data, addr = server.recvfrom(struct.calcsize('5iQ'))
                handle_client(data, addr, server, winner_numbers, history)
                winner_numbers = [random.randint(1, 20) for _ in range(5)]


if __name__ == "__main__":
    main()