import struct
import socket


def prepare(data):
    product, quantity = data.split()
    quantity = int(quantity)

    product += '-' * (20 - len(product))

    return struct.pack('i20si', len(product), product, quantity)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        tcp.connect(('localhost', 11111))  # 11111 is the proxy

        print('List (product + quantity):')

        data = input()
        while data != 'END 0':
            tcp.sendall(prepare(data))
            data = input()

        price = struct.unpack('i', tcp.recv(struct.calcsize('i')))[0]
        not_found = tcp.recv(256).decode()

        print(f'I have to pay {price} Forints.')
        print('Not found:', not_found)


if __name__ == "__main__":
    main()