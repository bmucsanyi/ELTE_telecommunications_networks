import socket
import struct # https://docs.python.org/3.7/library/struct.html
import _thread as thread
 
 
def get_values_from_calc_struct(s):
    packer = struct.Struct('i c i')
    return packer.unpack(s)

def create_result_struct(r):
    packer = struct.Struct('i')
    return packer.pack(r)

def recv_all(sock,length):
    buff = b''
    while length>0:
        b = sock.recv(length)
        length = length-len(b)
        buff = buff+b
    return buff

def handle_client(data, addr, sock):
    print("New client:",addr)

    s = data
    p1,op,p2 = get_values_from_calc_struct(s)
    op = op.decode()
    print(p1,op,p2)
    if op=="+":
        sock.sendto(create_result_struct(p1+p2),addr)
    elif op=="-":
        sock.sendto(create_result_struct(p1-p2),addr)
    elif op=="*":
        sock.sendto(create_result_struct(p1*p2),addr)
    elif op=="/":
        sock.sendto(create_result_struct(p1//p2),addr)

    print("Bye Client!")

# create sercver socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 5555))

while True:
    data, addr = s.recvfrom(4096)
    handle_client(data, addr,s)

s.close()
