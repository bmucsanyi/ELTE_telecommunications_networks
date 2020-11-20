import socket
import struct

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


def deliver_box(addr,box_id,data):
    s.sendto(pack_box(box_id,data),addr)
    success = False
    while not success:
        try:
            ack, _ = s.recvfrom(1024)
            success = unpack_ack(ack)==box_id
        except:
            s.sendto(pack_box(box_id,data),addr)

# ***** MAIN *****

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 5555))

# receive request
data, addr = s.recvfrom(1024)
fname = data.decode()
s.settimeout(5)

# start sending
with open(fname, "rb") as f:
    data = f.read(512)
    i = 0
    while data != b"":
        # deliver bytes
        deliver_box(addr,i,data)

        #read next bytes
        data = f.read(512)
        i+=1

    deliver_box(addr,i,b'')
    
s.close()