import struct
import socket
import sys


def pack(num_list, money):
    return struct.pack('5iQ', *num_list, money)


def unpack(resp):
    return struct.unpack('5iQ', resp)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        print('Money:')
        try:
            money = int(input('> '))
        except ValueError:
            print('invalid amount of money')
            sys.exit(-1)

        print('Numbers:')

        num_list = [int(input('> ')) for _ in range(5)]
        data = pack(num_list, money)

        udp.sendto(data, ('localhost', 22222))  # 22222 is the server

        resp, _ = udp.recvfrom(struct.calcsize('5iQ'))
        resp = unpack(resp)
        prize = resp[-1]
        winner_numbers = [num for num in resp[:-1]]

        print(f'You won {prize} dollars.')
        print('The winner numbers were', winner_numbers)


if __name__ == "__main__":
    main()