import socket

# client socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)

# send response
s.sendto("HELLO SERVER!\n".encode(), ("localhost", 5555))

# receive data
data, addr = s.recvfrom(4096)
print(addr, data.decode())

s.close()