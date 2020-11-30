import socket
import struct


def pack(price):
    return struct.pack('3si', b'BID', price)


def unpack(resp):
    return struct.unpack(f'3si', resp)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        tcp.connect(('localhost', 11111))  # 11111 is the server

        while True:
            input_ = input('BID <ár>: ')
            input_ = input_.strip().split()

            if input_[0] == 'exit':
                break
            elif input_[0] == 'BID':
                price = int(input_[1])
                data = pack(price)
                tcp.sendall(data)

                resp = tcp.recv(struct.calcsize('3si'), socket.MSG_WAITALL)

                if not resp:
                    print('end of licit')
                    break

                result, received_price = unpack(resp)

                print(f'received: ({result.decode()},{received_price})')
            else:
                print('unknown command')


if __name__ == "__main__":
    main()