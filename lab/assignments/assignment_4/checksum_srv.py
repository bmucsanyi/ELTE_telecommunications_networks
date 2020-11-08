import argparse
import select
import socket
import struct
import sys
import time


def handle_in_cmd(sock, checksum_dict):
    file_id, _, interval, _, length, _ = struct.unpack('icicic',
                                                       recvall(sock, 21))
    checksum = recvall(sock, length)
    checksum_dict[file_id] = (time.time() + interval, checksum)
    sock.sendall(b'OK')


def handle_out_cmd(sock, checksum_dict):
    file_id = struct.unpack('i', recvall(sock, 4))[0]  # always a tuple!

    try:
        timeout = checksum_dict[file_id][0]
        flag = file_id
    except KeyError:
        timeout = None
        flag = None

    if timeout is None or time.time() > timeout:
        message = struct.pack('ic', 0, b'|')
        if flag is not None:
            del checksum_dict[flag]
    else:
        checksum = checksum_dict[file_id][1]
        length = len(checksum)
        message = struct.pack(f'ic{length}s', length, b'|', checksum)
    sock.sendall(message)


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def run(args, verbose=True):
    checksum_dict = {}
    handler_dict = {b'BE|': handle_in_cmd, b'KI|': handle_out_cmd}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setblocking(False)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((args.ip, args.port))
        server.listen()

        inputs = [server]
        outputs = []  # unused
        timeout = 1

        while True:
            readable, _, _ = select.select(inputs, outputs, inputs, timeout)

            for sock in readable:
                if sock is server:
                    client_socket, client_addr = sock.accept()
                    if verbose:
                        print('New client:', client_addr)
                    inputs.append(client_socket)
                else:
                    # we read 4 instead of 3 because of padding
                    data = recvall(sock, 4)[:3]

                    if not data:
                        if verbose:
                            print('Bye client!')
                        inputs.remove(sock)
                        sock.close()
                    else:
                        handler_dict[data](sock, checksum_dict)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args(sys.argv[1:])

    run(args, verbose=False)


if __name__ == "__main__":
    main()
