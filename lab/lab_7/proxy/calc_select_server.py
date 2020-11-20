import socket
import struct  # https://docs.python.org/3.7/library/struct.html
import select


def get_values_from_calc_struct(s):
    packer = struct.Struct('ici')
    return packer.unpack(s)


def create_result_struct(r):
    packer = struct.Struct('i')
    return packer.pack(r)


def main():
    # create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)  # we can finally Ctrl + C out of it on Windows
    # the clients should set this very carefully...
    server.bind(("localhost", 5555))
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
            else:  # the original one was buggy
                data = s.recv(12)
                if not data:  # CTRL + C
                    print("Bye bye client!")
                    inputs.remove(s)
                    s.close()
                    break
                p1, op, p2 = get_values_from_calc_struct(data)
                op = op.decode()
                print(p1, op, p2)
                if op == "+":
                    s.sendall(create_result_struct(p1 + p2))
                elif op == "-":
                    s.sendall(create_result_struct(p1 - p2))
                elif op == "*":
                    s.sendall(create_result_struct(p1 * p2))
                elif op == "/":
                    s.sendall(create_result_struct(p1 // p2))


if __name__ == "__main__":
    main()