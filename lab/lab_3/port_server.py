import socket
import sys


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 0
    server_addr = ('localhost', port)

    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1)

    print(f"Connected to port {server.getsockname()[1]}.")

    while True:
        try:
            client, client_addr = server.accept()

            print("Csatlakozott:", client_addr)

            data = client.recv(16)
            print("Kaptam:", data)
            print("Kaptam dekódolva:", data.decode())

            client.sendall("Hello kliens".encode())

            client.close()
        except socket.timeout as p:
            # print(p)
            pass
        except socket.error as e:
            print(e)


if __name__ == "__main__":
    main()