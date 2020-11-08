import argparse
import select
import socket
import struct
import sys
import time


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def handle_in_cmd(sock, checksum_dict):
    data = b''
    counter = 0
    while True:
        chunk = sock.recv(1)
        if chunk == b'|': counter += 1
        if counter == 3:
            length = int(data.decode().split('|')[-1])
            data += chunk
            chunk = recvall(sock, length)
            data += chunk
            break
        data += chunk

    file_id, interval, _, checksum = data.decode().split('|')
    file_id = int(file_id)
    interval = int(interval)

    checksum_dict[file_id] = (time.time() + interval, checksum)
    sock.sendall(b'OK')


def handle_out_cmd(sock, checksum_dict):
    data = sock.recv(20)  # Max. 20 length, limitation!
    file_id = int(data.decode())

    try:
        timeout = checksum_dict[file_id][0]
        flag = file_id
    except KeyError:
        timeout = None
        flag = None

    if timeout is None or time.time() > timeout:
        message = b'0|'
        if flag is not None:
            del checksum_dict[flag]
    else:
        checksum = checksum_dict[file_id][1]
        message = f'{len(checksum)}|{checksum}'.encode()
    sock.sendall(message)


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
                    data = recvall(sock, 3)
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
