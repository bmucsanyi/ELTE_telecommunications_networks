import socket
import sys

class PortError(Exception):
    pass


def main():
    try:
        server_addr = ('localhost', int(sys.argv[1]))
    except IndexError:
        raise PortError("No port value provided! Exiting...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(server_addr)

        print("Send hello")
        client.sendall("Hello szerver".encode())

        data = client.recv(16).decode()
        print("Kaptam:", data)


if __name__ == "__main__":
    main()