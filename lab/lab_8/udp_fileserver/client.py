import socket
import struct
import sys

# ***** HELPER FUNCTIONS *****

def pack_box(box_id,data):
    packer = struct.Struct("Q i 512s")
    pad = b'X'*(512-len(data))
    return packer.pack(box_id,len(data),data+pad)

def unpack_box(msg):
    packer = struct.Struct("Q i 512s")
    box_id, data_len, data = packer.unpack(msg)
    return box_id, data[:data_len]

def pack_ack(box_id):
    packer = struct.Struct("Q")
    return packer.pack(box_id)

def unpack_ack(msg):
    packer = struct.Struct("Q")
    box_id = packer.unpack(msg)
    return box_id[0]

host = sys.argv[1]
fname = sys.argv[2]

local_file = open("received_"+fname, "wb")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(fname.encode(),(host,5555))

msg, _ = s.recvfrom(1024)
box_id, data = unpack_box(msg)
s.sendto(pack_ack(box_id),(host,5555))
last_id = -1

while data!=b'':
    # write to local file
    if last_id != box_id:
        print(data)
        local_file.write(data)
        last_id = box_id

    # receive next box
    msg, _ = s.recvfrom(1024)
    box_id, data = unpack_box(msg)
    s.sendto(pack_ack(box_id),(host,5555))

local_file.close()
s.close()


