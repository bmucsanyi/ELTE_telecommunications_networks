import socket
import select


def main():
    # create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)  # we don't have to block, select does everything
    # equal to setblocking(0) or settimeout(0.0)
    server.bind(("localhost", 5555))  # terminálban nc localhost 5555
    server.listen(1)

    inputs = [server]
    outputs = []
    timeout = 1

    while True:
        # select what is ready
        readable, _, _ = select.select(inputs, outputs, inputs,
                                                        timeout)

        # processing
        for s in readable:
            if s is server:
                client_socket, client_addr = s.accept()
                print("New client:", client_addr)
                inputs.append(client_socket)
            else:
                data = s.recv(1024)
                if len(data) == 0:
                    print("Client left:", s.getpeername())
                    inputs.remove(s)
                    continue
                print("Message from", s.getpeername())
                print("\t", data)
                s.sendall("OK".encode("UTF-8"))


if __name__ == "__main__":
    main()