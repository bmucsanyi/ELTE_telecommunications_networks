import argparse
import sys
import socket
import struct
import hashlib
import time

def create_in_struct(file_id, time, length, checksum):
    return struct.pack(f'3sicicic{length}s', b'BE|', file_id, b'|', time, b'|',
                       length, b'|', checksum)


def create_out_struct(file_id):
    return struct.pack('3si', b'KI|', file_id)


def send_file(args, verbose=True):
    md5 = hashlib.md5()

    with open(args.file_path, 'rb') as f:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((args.srv_ip, args.srv_port))

            while True:
                chunk = f.read(1024)
                if not chunk:
                    break  # EOF
                client.sendall(chunk)
                md5.update(chunk)

    if verbose:
        print('Finished sending data.')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((args.chsum_srv_ip, args.chsum_srv_port))
        checksum = md5.digest()
        in_struct = create_in_struct(args.file_id, 60, len(checksum),
                                     checksum)
        client.sendall(in_struct)

    if verbose:
        print('Finished sending checksum.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('srv_ip', type=str)
    parser.add_argument('srv_port', type=int)
    parser.add_argument('chsum_srv_ip', type=str)
    parser.add_argument('chsum_srv_port', type=int)
    parser.add_argument('file_id', type=int)
    parser.add_argument('file_path', type=str)
    args = parser.parse_args(sys.argv[1:])

    send_file(args, verbose=False)
