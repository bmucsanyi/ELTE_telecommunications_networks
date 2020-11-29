import struct
import socket
import sys


def pack(num_list, money):
    return struct.pack('5iQ', *num_list, money)


def unpack(resp):
    return struct.unpack('5iQ', resp)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(5)

        print('Money:')
        try:
            money = int(input('> '))
        except ValueError:
            print('invalid amount of money')
            sys.exit(-1)

        print('Numbers:')

        num_list = [int(elem) for elem in input('> ').split()]

        if len(num_list) != 5:
            raise ValueError('invalid tips')
            sys.exit(-1)

        data = pack(num_list, money)

        udp.sendto(data, ('localhost', 22222))  # 22222 is the server

        try:
            resp, _ = udp.recvfrom(struct.calcsize('5iQ'))
            resp = unpack(resp)
            prize = resp[-1]
            winner_numbers = [num for num in resp[:-1]]

            print(f'You won {prize} dollars.')
            print('The winner numbers were', winner_numbers)
        except socket.timeout:
            print('no response from server')


if __name__ == "__main__":
    main()