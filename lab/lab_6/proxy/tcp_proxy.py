"""General tcp proxy template.

Doesn't work with http requests."""

import socket
import select

proxy_destination = ("localhost", 5555)

proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_server.setblocking(0)
proxy_server.bind(("localhost", 8888))
proxy_server.listen(10)

inputs = [proxy_server]
outputs = []
timeout = 1

proxy_inputs = []
proxy_outputs = []

in_to_out = {}
out_to_in = {}

while True:
    # select what is ready
    readable, writable, exceptional = select.select(inputs, outputs, inputs,
                                                    timeout)

    # processing
    for s in readable:
        if s is proxy_server:
            client_socket, client_addr = s.accept()
            print("New client:", client_addr)
            inputs.append(client_socket)
            proxy_inputs.append(client_socket)

            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(proxy_destination)
            inputs.append(conn)
            proxy_outputs.append(conn)

            in_to_out[client_socket] = conn
            out_to_in[conn] = client_socket

        else:
            data = s.recv(1024)
            print(s.getpeername(), data)
            
            if s in proxy_inputs:
                conn = in_to_out[s]

                if len(data) == 0:
                    print("Client left:", s.getpeername())
                    inputs.remove(s)
                    proxy_inputs.remove(s)
                    conn.close()
                    inputs.remove(conn)
                    proxy_outputs.remove(conn)
                    del in_to_out[s]
                    del out_to_in[conn]
                else:
                    conn.sendall(data)
            else:
                inp = out_to_in[s]

                if len(data) == 0:
                    print("Output closed:", s.getpeername())
                    inp.close()
                    inputs.remove(s)
                    inputs.remove(inp)
                    proxy_inputs.remove(inp)
                    proxy_outputs.remove(s)
                    del in_to_out[inp]
                    del out_to_in[s]
                else:
                    inp.sendall(data)
