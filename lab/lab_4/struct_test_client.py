import socket
import struct
import time


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 5555))

    print("### Test 1")
    s.sendall(struct.pack("i i", 0, 255))
    input()

    print("### Test 2")
    s.sendall(struct.pack("i", 0))
    time.sleep(1)
    s.sendall(struct.pack("i", 255))
    input()

    print("### Test 3")
    s.sendall(struct.pack("i", 0))
    s.sendall(struct.pack("i", 255))


if __name__ == "__main__":
    main()