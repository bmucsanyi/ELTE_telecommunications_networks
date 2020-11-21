import socket

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.settimeout(5)

tcp_socket.bind(("localhost", 6666))
tcp_socket.listen()

# works with only one client
client_tcp, client_addr = tcp_socket.accept()
print("New client:", client_addr)

for i in range(10):  # simulating crash of proxy
    data = client_tcp.recv(12)  # !!!
    udp_socket.sendto(data, ("localhost", 5555))
    try:
        resp, _ = udp_socket.recvfrom(12)  # !!!
    except socket.timeout:
        resp = b""
        break
    client_tcp.send(resp)

client_tcp.close()
tcp_socket.close()
udp_socket.close()
