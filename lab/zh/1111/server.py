import random
import socket


def handle_client(data, addr, sock, winner_numbers):
    print('New client:', addr)

    data = data.decode().split(':')
    money = int(data[-1])
    tips = [int(num) for num in data[:-1]]
    
    good_tips = len(set(tips) & set(winner_numbers))

    num_list = map(str, winner_numbers + [money * good_tips])
    data = ':'.join(num_list).encode()

    sock.sendto(data, addr)

    return [random.randint(1, 20) for _ in range(5)]


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', 22222))

        winner_numbers = [random.randint(1, 20) for _ in range(5)]
        while True:
            data, addr = server.recvfrom(4096)
            winner_numbers = handle_client(data, addr, server, winner_numbers)


if __name__ == "__main__":
    main()