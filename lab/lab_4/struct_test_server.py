import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 5555))
    s.listen()
    print("Ready...")

    client_sock, _ = s.accept()  # second retval is the client_addr

    print("### Test 1")
    data = client_sock.recv(8)
    print(data, len(data))

    print("### Test 2")
    data = client_sock.recv(8)
    print(data, len(data))
    data = client_sock.recv(8)
    print(data, len(data))

    print("### Test 3")
    data = client_sock.recv(8, socket.MSG_WAITALL)
    print(data, len(data))

    s.close()


if __name__ == "__main__":
    main()