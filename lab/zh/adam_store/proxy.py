import select
import socket
import struct


def main():
    stock = {'alma': 200, 'korte': 100, 'barack': 300, 'monitor': 70000}
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.settimeout(5)

            tcp.setblocking(False)
            tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp.bind(('localhost', 11111))
            tcp.listen(1)

            inputs = [tcp]
            outputs = []
            timeout = 1

            client2list = {}

            while True:
                readable, _, _ = select.select(inputs, outputs, inputs,
                                                timeout)

                for s in readable:
                    if s is tcp:
                        client_socket, client_addr = s.accept()
                        print('New client:', client_addr)
                        inputs.append(client_socket)
                        client2list[client_socket] = ([], [])
                    else:
                        length = struct.unpack('i', s.recv(struct.calcsize('i')))[0]

                        product = s.recv(20).decode()
                        product = product[:length]
                        quantity = struct.unpack('i', s.recv(struct.calcsize('i')))[0]

                        if product == 'END':
                            to_send = client2list[s][1]
                            if len(to_send):
                                # data = struct.pack(f'i{len(to_send)}i', len(to_send), *to_send)
                                # this doesn't work with udp on the server side
                                # TCP works like a stream: you can read it in steps you prefer
                                # UDP works with DGRAM: you get packages into your buffer
                                # and if you read a bit of a package, the rest gets thrown away
                                data = struct.pack('i', len(to_send))
                                udp.sendto(data, ('localhost', 22222))
                                data = struct.pack(f'{len(to_send)}i', *to_send)
                                udp.sendto(data, ('localhost', 22222))

                                try:
                                    resp = udp.recvfrom(struct.calcsize('i'))[0]
                                    s.sendall(resp)
                                    s.sendall(','.join(client2list[s][0]).encode())
                                except socket.timeout:
                                    print('no answer from server')
                            else:
                                s.sendall(struct.pack('i', 0))
                                s.sendall(','.join(client2list[s][0]).encode())

                            inputs.remove(s)
                            del client2list[s]
                            s.close()
                        else:
                            if product in stock.keys():
                                client2list[s][1].append(stock[product] * quantity)
                            else:
                                client2list[s][0].append(product)


if __name__ == "__main__":
    main()