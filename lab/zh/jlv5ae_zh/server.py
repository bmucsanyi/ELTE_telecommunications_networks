import socket
import struct
import select


def unpack(req):
    return struct.unpack('3si', req)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setblocking(False)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 11111))
        server.listen(3)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as log:
            inputs = [server]
            outputs = []
            timeout = 1

            max_price = 2000  # kikiáltási ár
            readable = []

            done = False
            while not done:
                readable, _, _ = select.select(inputs, outputs, inputs,
                                                                timeout)

                for s in readable:
                    if s is server:
                        client_socket, client_addr = s.accept()
                        print("New client:", client_addr)
                        inputs.append(client_socket)
                    else:
                        data = s.recv(struct.calcsize('3si'))
                        if not data:
                            inputs.remove(s)
                            s.close()
                            continue

                        cmd, price = unpack(data)
                        if cmd != b'BID':
                            print('unknown command received')
                        else:
                            if price > max_price:
                                max_price = price
                                log.sendto(struct.pack('i', price), ('localhost', 22222))

                                if price >= 10**6:
                                    print('end of licit')
                                    done = True
                                    break
                                else:
                                    s.sendall(struct.pack('3si', b'OK ', price))
                            else:
                                s.sendall(struct.pack('3si', b'LOW', max_price))


if __name__ == "__main__":
    main()