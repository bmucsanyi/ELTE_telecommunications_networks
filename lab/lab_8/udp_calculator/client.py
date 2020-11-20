import socket
import struct # https://docs.python.org/3.7/library/struct.html

def create_calc_struct(p1,op,p2):
    packer = struct.Struct('i c i')
    return packer.pack(p1,op,p2)

def get_result_from_struct(s):
    packer = struct.Struct('i')
    return packer.unpack(s)[0]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)

while True:
    # read command
    print("New calculation")
    p1 = int(input("\tparam1> "))
    op = input("\toperator> ")
    p2 = int(input("\tparam2> "))
    
    # send to the server
    cs = create_calc_struct(p1,op.encode(),p2)
    s.sendto(cs,("localhost",5555))
    if op=="X":
        break

    # receive answer
    try:
        resp, addr = s.recvfrom(4096)
        result = get_result_from_struct(resp)
        print("Result:",result,"\n")
    except:
        print("Nem jött válasz.")

s.close()


