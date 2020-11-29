import socket
import struct
import hashlib


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', 22222))

        while True:
            req, addr = server.recvfrom(struct.calcsize('i'))
            length = struct.unpack('i', req)[0]

            num_list = struct.unpack(f'{length}i', server.recvfrom(struct.calcsize(f'{length}i'))[0])
            result = sum(num_list)

            server.sendto(struct.pack('i', result), addr)


if __name__ == "__main__":
    main()