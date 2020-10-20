import argparse
import random
import select
import socket
import struct
import sys

NUM_RANGE = (1, 100)


def create_result_struct(comp, num):
    return struct.pack('ci', comp, num)


def get_guess_from_struct(struct_):
    return struct.unpack('ci', struct_)


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def moderate_game(args, verbose=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setblocking(False)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((args.server_address, args.server_port))
        server.listen()

        inputs = [server]
        outputs = []  # unused
        timeout = 1

        while True:
            found = False
            secret = random.randint(1, 100)

            if verbose:
                print('New secret:', secret)

            while not found:
                readable, _, _ = select.select(inputs, outputs, inputs,
                                               timeout)

                for sock in readable:
                    if sock is server:
                        client_socket, client_addr = sock.accept()
                        if verbose:
                            print('New client:', client_addr)
                        inputs.append(client_socket)
                    else:
                        data = recvall(sock, 8)
                        if not data:
                            if verbose:
                                print('Bye client!')
                                inputs.remove(sock)
                                sock.close()
                        else:
                            comp, num = get_guess_from_struct(data)
                            comp = comp.decode()

                            if verbose:
                                print('Got:', comp, num, sock.getpeername())

                            if comp == '=':
                                if secret == num:
                                    found = True
                                    result_char = 'Y'

                                    if verbose:
                                        print('We have a winner:',
                                              sock.getpeername())
                                        # from the perspective of the server,
                                        # the winner is the peer
                                else:
                                    result_char = 'K'
                                result = create_result_struct(
                                    result_char.encode(), 0)
                                sock.sendall(result)
                                inputs.remove(sock)
                                sock.close()
                            else:
                                if comp == '<':
                                    result_char = 'I' if secret < num else 'N'
                                else:
                                    result_char = 'I' if secret > num else 'N'
                                result = create_result_struct(
                                    result_char.encode(), 0)
                                sock.sendall(result)
            inputs.remove(server)
            for sock in inputs:  # we don't have to read from them
                result = create_result_struct(b'V', 0)
                sock.sendall(result)
                sock.close()

            inputs = [server]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_address', type=str)
    parser.add_argument('server_port', type=int)
    args = parser.parse_args(sys.argv[1:])

    moderate_game(args, verbose=True)


if __name__ == "__main__":
    main()