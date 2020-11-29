import random
import socket
import struct
import select


def pack(num_list):
    return struct.pack(f'{len(num_list)}i', *num_list)


def unpack(req):
    return struct.unpack('i', req)[0]


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setblocking(False)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 11111))
        server.listen(3)

        inputs = [server]
        outputs = []
        timeout = 1

        while True:
            readable, _, _ = select.select(inputs, outputs, inputs,
                                                            timeout)

            for s in readable:
                if s is server:
                    client_socket, client_addr = s.accept()
                    print("New client:", client_addr)
                    inputs.append(client_socket)
                else:
                    data = s.recv(4)
                    if not data:  # CTRL + C
                        inputs.remove(s)
                        s.close()
                        continue
                    num = unpack(data)
                    num_list = [random.randint(1, 100) for _ in range(num)]
                    resp = pack(num_list)
                    s.sendall(resp)


if __name__ == "__main__":
    main()