import socket

# client socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)  # Sets a timeout on all blocking operations.
# This is for both TCP and UDP.

# send response
# The method sendto() of the Python's socket class, is used to send datagrams to a UDP socket.
s.sendto("HELLO SERVER!\n".encode(), ("localhost", 5555))  # doesn't block

# receive data
data, addr = s.recvfrom(4096)  # blocks: waits 5s, then raises socket.timeout
print(addr, data.decode())

s.close()