import argparse
import sys
import hashlib
import socket
import struct


def create_out_msg(file_id):
    message = f'KI|{file_id}'.encode()
    return message


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def test_checksum(calculated_checksum, client):
    # data = recvall(client, 5)
    data = b''
    while True:
        chunk = client.recv(1)
        if chunk == b'|':
            length = int(data.decode())
            break
        data += chunk

    real_checksum = recvall(client, length).decode()

    if real_checksum == calculated_checksum:
        print('CSUM OK')
    else:
        print('CSUM CORRUPTED')


def handle_client(args, verbose=True):
    md5 = hashlib.md5()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((args.srv_ip, args.srv_port))
        server.listen()

        client_socket, client_addr = server.accept()
        if verbose:
            print('New client:', client_addr)

        with open(args.file_path, 'wb') as f:
            while True:
                data = client_socket.recv(1024)  # recvall(client_socket, 1024)
                if not data:  # not "not None"!!!
                    break
                f.write(data)
                md5.update(data)

        if verbose:
            print('Finished writing data.')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
         client.connect((args.chsum_srv_ip, args.chsum_srv_port))
         out_msg = create_out_msg(args.file_id)
         client.sendall(out_msg)
         test_checksum(md5.hexdigest(), client)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('srv_ip', type=str)
    parser.add_argument('srv_port', type=int)
    parser.add_argument('chsum_srv_ip', type=str)
    parser.add_argument('chsum_srv_port', type=int)
    parser.add_argument('file_id', type=int)
    parser.add_argument('file_path', type=str)
    args = parser.parse_args(sys.argv[1:])

    handle_client(args, verbose=False)