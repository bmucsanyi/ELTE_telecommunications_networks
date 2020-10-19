import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", int(sys.argv[1])))
s.listen()

while True:
    client_socket, client_addr = s.accept()
    try:
        req = b''
        while True:
            data = client_socket.recv(1024)
            print(data)
            req = req + data
            if data[-1] == 0 and data[-1] == 0:
                break
            if data[-4:] == "\r\n\r\n".encode():
                break
            if data[-2:] == "\n\n".encode():
                break
            if len(data) == 0:
                break
        req = req.decode()
        req = req.replace("localhost:" + str(sys.argv[1]), sys.argv[2])
        req = req.replace("localhost", sys.argv[2])
        print(req)
        #keep = "keep-alive" in req

        proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_sock.connect((sys.argv[2], int(sys.argv[3])))
        proxy_sock.sendall(req.encode())
        proxy_sock.settimeout(0.1)
        while True:
            data = proxy_sock.recv(1024)
            #print(data)
            client_socket.send(data)
            if len(data) == 0:
                break
        proxy_sock.close()
    except Exception as e:
        print(e)
    client_socket.close()
