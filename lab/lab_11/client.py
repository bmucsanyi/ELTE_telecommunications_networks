import socket
import struct


def pack(num):
    return struct.pack('i', num)


def unpack(resp, num):
    return struct.unpack(f'{num}i', resp)



def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            tcp.connect(('localhost', 11111))
            udp.settimeout(5)

            while True:
                input_ = input('> ')
                input_ = input_.strip().split()

                if input_[0] == 'exit':
                    break
                elif input_[0] == 'ask':
                    num = int(input_[1])
                    data = pack(num)
                    tcp.sendall(data)

                    resp = tcp.recv(num * 4, socket.MSG_WAITALL)
                    result = unpack(resp, num)

                    print('random numbers:', list(result))

                    udp.sendto(b'help', ('localhost', 22222))
                    try:
                        resp, _ = udp.recvfrom(4)
                        extra_num = struct.unpack('i', resp)[0]

                        print('extra number:', extra_num)
                        full_value = sum(result) + extra_num
                        print('result:', full_value)

                        if full_value >= 500:
                            print('I AM SO HAPPY\n')
                        else:
                            print()
                    except socket.timeout:
                        print('no response from hope server')
                else:
                    print('unknown command')


if __name__ == "__main__":
    main()