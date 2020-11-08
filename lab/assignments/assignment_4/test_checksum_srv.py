import socket
import struct
import time


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def create_in_msg(file_id, time, length, checksum):
    message = f'BE|{file_id}|{time}|{length}|{checksum}'.encode()
    return message


def create_out_msg(file_id):
    message = f'KI|{file_id}'.encode()
    return message


def main():
    # TODO: Unittestify this. :)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 10101))

        in_msg = create_in_msg(1237671, 60, 12, 'abcdefabcdef')
        sock.sendall(in_msg)

        resp = recvall(sock, 2)

        assert resp == b'OK'
        print('resp was OK')

        out_msg = create_out_msg(123)
        sock.sendall(out_msg)

        resp = recvall(sock, 2)

        assert resp == b'0|'
        print('resp was OK')

        out_msg = create_out_msg(1237671)
        sock.sendall(out_msg)

        resp = sock.recv(15)  # recvall(sock, 15)

        assert resp == b'12|abcdefabcdef'
        print('resp was OK')

        out_msg = create_out_msg(1237671)
        time.sleep(65)
        sock.sendall(out_msg)

        resp = recvall(sock, 2)

        assert resp == b'0|'
        print('resp was OK')


if __name__ == '__main__':
    main()