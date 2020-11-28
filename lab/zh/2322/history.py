import hashlib
import json
import os
import select
import socket
import struct


def unpack_history(data):
    return struct.unpack('10iQ', data)


def check_checksum(received_checksum, data):
    md5 = hashlib.md5()
    md5.update(data)

    return received_checksum == md5.digest()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        tcp.setblocking(False)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind(("localhost", 11111))
        tcp.listen(1)

        inputs = [tcp]
        outputs = []
        timeout = 1

        while True:
            readable, _, _ = select.select(inputs, outputs, inputs,
                                            timeout)

            for s in readable:
                if s is tcp:
                    client_socket, client_addr = s.accept()
                    print("New client:", client_addr)
                    inputs.append(client_socket)
                else:
                    data = s.recv(struct.calcsize('10iQ') + 16)
                    if not data:
                        inputs.remove(s)
                        s.close()
                        continue

                    received_checksum = data[-16:]
                    data = data[:-16]

                    if not check_checksum(received_checksum, data):
                        print('Invalid data received!')
                        print('Dropping package...')
                        continue

                    data = unpack_history(data)
                    winner_numbers = data[:5]
                    tips = data[5:10]
                    prize = data[-1]

                    if os.path.isfile('log.json'):
                        with open('log.json') as f:
                            log = json.load(f)
                            log['winner_numbers'].append(winner_numbers)
                            log['tips'].append((tips, prize))
                        with open('log.json', 'w') as f:
                            json.dump(log, f)
                    else:
                        with open('log.json', 'w') as f:
                            log = {}
                            log['winner_numbers'] = [winner_numbers]
                            log['tips'] = [(tips, prize)]
                            json.dump(log, f)


if __name__ == "__main__":
    main()