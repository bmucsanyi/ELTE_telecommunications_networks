import socket
import struct
import sys

# ***** HELPER FUNCTIONS *****


def unpack_box(msg):
    packer = struct.Struct("Q i 512s")
    box_id, data_len, data = packer.unpack(msg)
    return box_id, data[:data_len]


def pack_ack(box_id):
    packer = struct.Struct("Q")
    return packer.pack(box_id)


host = sys.argv[1]
fname = sys.argv[2]

local_file = open("received_" + fname, "wb")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(fname.encode(), (host, 5555))

msg, _ = s.recvfrom(1024)
box_id, data = unpack_box(msg)
s.sendto(pack_ack(box_id), (host, 5555))

while data != b'':
    # write to local file
    print(data)
    local_file.write(data)

    # receive next box
    msg, _ = s.recvfrom(1024)
    box_id, data = unpack_box(msg)
    s.sendto(pack_ack(box_id), (host, 5555))

local_file.close()
s.close()

# Megj.: Ha mindig csak a nyugta veszik el, akkor a szerver nagyon sok
# duplikátumot fog küldeni, ezáltal a célfájlunk nem lesz jó.
