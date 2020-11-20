import socket
import struct  # https://docs.python.org/3.7/library/struct.html


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
    # connect blocks in the case of tcp (udp doesn't even need it)
    s.connect(("localhost", 5555))

    while True:
        # read command
        print("New calculation")
        p_1 = int(input("\tparam1> "))
        op = input("\toperator> ")
        p_2 = int(input("\tparam2> "))

        # send to the server
        if op == "X":
            s.close()
            # Sockets are automatically closed when they are garbage-collected,
            # but it is recommended to close() them explicitly, or to use a
            # with statement around them.
            break
        cs = create_calc_struct(p_1, op.encode(), p_2)
        s.sendall(cs)

        # receive answer
        resp = s.recv(4)  # we want to receive at most four bytes!!!
        result = get_result_from_struct(resp)
        print("Result:", result, "\n")


if __name__ == "__main__":
    main()