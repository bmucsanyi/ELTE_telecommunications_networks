import socket
import json
import select


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        tcp.setblocking(False)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind(("localhost", 11111))
        tcp.listen(1)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
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
                        data = s.recv(256)
                        if not data:
                            inputs.remove(s)
                            s.close()
                            break
                        udp.sendto(data, ("localhost", 22222))
                        data = data.decode().split(':')
                        tips = [int(num) for num in data[:-1]]


                        resp = udp.recvfrom(256)
                        resp = resp.decode().split(':')
                        prize = int(resp[-1])
                        winner_numbers = [int(num) for num in resp[:-1]]

                        with open('log.json', 'r') as f:
                            log = json.load(f)
                            if not len(log):
                                log['winner_numbers'] = [winner_numbers]
                                log['tips'] = [(tips, prize)]
                            else:
                                log['winner_numbers'].append(winner_numbers)
                                log['tips'].append((tips, prize))
                        with open('log.json', 'w') as f:
                            json.dump(log, f)

                        tcp.sendall(resp)

if __name__ == "__main__":
    main()