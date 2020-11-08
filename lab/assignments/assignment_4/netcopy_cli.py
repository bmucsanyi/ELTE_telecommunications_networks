import argparse
import sys
import socket
import hashlib
import time

def create_in_msg(file_id, time, length, checksum):
    message = f'BE|{file_id}|{time}|{length}|{checksum}'.encode()
    return message


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
        checksum = md5.hexdigest()
        in_msg = create_in_msg(args.file_id, 60, len(checksum),
                                  checksum)
        client.sendall(in_msg)

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
