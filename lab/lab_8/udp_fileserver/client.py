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
last_id = -1

while data != b'':
    # write to local file
    if box_id == last_id + 1:
        print(data)
        local_file.write(data)
        last_id = box_id

    # receive next box
    msg, _ = s.recvfrom(1024)
    box_id, data = unpack_box(msg)
    s.sendto(pack_ack(box_id),
             (host, 5555))  # nyugtát duplikátumnál is küldünk

local_file.close()
s.close()

# Megj. 1: lehet, hogy sokszor veszik el a nyugta, ezért sokszor küldi el
# feleslegesen a szerver az adott adatrészletet.

# Megj. 2: a recvfrom-hoz itt nem kell try-except blokk, ugyanis ha esetleg
# elveszne a csomag utazás közben, a szerver rájönne a nyugta hiányából
# és újraküldené, tehát előbb-utóbb kijönnénk a blokkolt állapotból.

# Megj. 3: most 1 csomaghoz 1 nyugta tartozik, így az nem fordulhat elő, hogy rossz sorrendben érkeznek meg a csomagok. Ha több csomaghoz tartozna 1 nyugta, akkor ezzel is meg kéne küzdenünk.
