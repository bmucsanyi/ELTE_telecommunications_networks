import socket
import struct
import json

MAX_JSON_LENGTH = 1020
JSON_STRUCT_SIZE = MAX_JSON_LENGTH + 4

packer = struct.Struct("i " + str(MAX_JSON_LENGTH) + "s")


def dict_to_jsonstruct(d):
    s = json.dumps(d)
    l = len(s)
    return packer.pack(l, s.encode("utf-8"))


def jsonstruct_to_dict(s):
    d = packer.unpack(s)
    return json.loads(d[1][0:d[0]].decode("utf-8"))


# server socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 5555))

# receive data
data, addr = s.recvfrom(4096)
print(addr, data.decode())

# send response
s.sendto("HELLO CLIENT!\n".encode(), addr)

s.close()
