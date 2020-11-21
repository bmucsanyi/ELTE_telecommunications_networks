import socket
import struct  # https://docs.python.org/3.7/library/struct.html


def create_calc_struct(p1, op, p2):
    packer = struct.Struct('i c i')
    return packer.pack(p1, op, p2)


def get_result_from_struct(s):
    packer = struct.Struct('i')
    return packer.unpack(s)[0]


# connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 6666))  # connect to proxy

while True:
    # read command
    print("New calculation")
    p1 = int(input("\tparam_1> "))
    op = input("\toperator> ")
    p2 = int(input("\tparam_2> "))

    # send to the server
    cs = create_calc_struct(p1, op.encode(), p2)
    s.sendall(cs)
    if op == "X":
        break

    # receive answer
    resp = s.recv(4)  # !!!
    if len(resp) == 0:  # if not resp:
        print("LOST response")
        break
    result = get_result_from_struct(resp)
    print("Result:", result, "\n")
