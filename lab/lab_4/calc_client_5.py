import socket
import struct  # https://docs.python.org/3.7/library/struct.html
import random
import time


def create_calc_struct(p_1, op, p_2):
    # packer = struct.Struct('ici')
    # return packer.pack(p1, op, p2)
    return struct.pack('ici', p_1, op, p_2)


def get_result_from_struct(s):
    # packer = struct.Struct('i')
    # return packer.unpack(s)[0]
    return struct.unpack('i', s)[0]  # it always returns a tuple



def main():
    # connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # standard tcp connection
    s.connect(("localhost", 5555))  # connect blocks in the case of tcp
    # s.setblocking(False)  # would be problematic at s.recv(4),
    # as it couldn't be served immediately.

    for i in range(1, 6):
        p_1 = random.randint(1, 100)
        op = random.choice(["+", "-", "*", "/"])
        p_2 = random.randint(1, 100)
        print(f"Calculation {i}: {p_1} {op} {p_2}")

        cs = create_calc_struct(p_1, op.encode(), p_2)
        s.sendall(cs)

        time.sleep(2)  # we could uncomment it and it would work just fine!

        # receive answer
        resp = s.recv(4)  # we want to receive exactly four bytes!
        result = get_result_from_struct(resp)
        print("Result:", result, "\n")

    s.close()


if __name__ == "__main__":
    main()