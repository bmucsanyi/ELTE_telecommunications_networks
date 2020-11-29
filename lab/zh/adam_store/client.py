import struct
import socket


def prepare(data):
    product, quantity = data.split()
    quantity = int(quantity)

    length = len(product)
    product += '-' * (20 - len(product))
    product = product.encode()

    return struct.pack('i20si', length, product, quantity)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        tcp.connect(('localhost', 11111))  # 11111 is the proxy

        print('List (product + quantity):')

        data = input()
        while True:
            tcp.sendall(prepare(data))
            if data == 'END 0':
                break
            data = input()

        price = struct.unpack('i', tcp.recv(struct.calcsize('i')))[0]
        not_found = tcp.recv(256).decode()

        print(f'I have to pay {price} Forints.')
        print('Not found:', not_found)


if __name__ == "__main__":
    main()