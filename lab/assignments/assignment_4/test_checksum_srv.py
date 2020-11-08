import socket
import struct
import time


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def create_in_struct(file_id, time, length, checksum):
    return struct.pack(f'3sicicic{length}s', b'BE|', file_id, b'|', time, b'|',
                       length, b'|', checksum)


def create_out_struct(file_id):
    return struct.pack('3si', b'KI|', file_id)


def main():
    # TODO: Unittestify this. :)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 10101))

        in_struct = create_in_struct(1237671, 60, 12, b'abcdefabcdef')
        sock.sendall(in_struct)

        resp = recvall(sock, 2)

        assert resp == b'OK'
        print('resp was OK')

        out_struct = create_out_struct(123)
        sock.sendall(out_struct)

        resp = struct.unpack('ic', recvall(sock, 5))

        assert resp == (0, b'|')
        print('resp was OK')

        out_struct = create_out_struct(1237671)
        sock.sendall(out_struct)

        resp = struct.unpack('ic12s', recvall(sock, 17))

        assert resp == (12, b'|', b'abcdefabcdef')
        print('resp was OK')

        out_struct = create_out_struct(1237671)
        time.sleep(65)
        sock.sendall(out_struct)

        resp = struct.unpack('ic', recvall(sock, 5))

        assert resp == (0, b'|')
        print('resp was OK')


if __name__ == '__main__':
    main()