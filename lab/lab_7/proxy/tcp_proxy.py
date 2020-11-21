"""General tcp proxy template.

Doesn't work with http requests."""

import socket
import select

# proxy_destination = ("localhost", 5555)
proxy_destination = ("www.web.mit.edu", 80)

proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_server.setblocking(False)
# bind() is used to associate the socket with the server address
proxy_server.bind(("localhost", 8888))
# calling listen() puts the socket into server mode,
# and accept() waits for an incoming connection
proxy_server.listen(10)
# when you call sock.listen(n) and (n + m) connection requests come in
# before you call accept, m of them are getting dropped

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
            data = s.recv(1024)  # global maximum
            # Returns the remote address to which the socket is connected.
            print(s.getpeername(), data)

            if s in proxy_inputs:
                conn = in_to_out[s]

                if len(data) == 0:
                    print("Client left:", s.getpeername())
                    inputs.remove(s)
                    proxy_inputs.remove(s)
                    s.close()
                    inputs.remove(conn)
                    proxy_outputs.remove(conn)
                    conn.close()
                    del in_to_out[s]
                    del out_to_in[conn]
                else:
                    conn.sendall(data)
            else:
                inp = out_to_in[s]

                if len(data) == 0:
                    print("Output closed:", s.getpeername())
                    inp.close()
                    s.close()
                    inputs.remove(s)
                    inputs.remove(inp)
                    proxy_inputs.remove(inp)
                    proxy_outputs.remove(s)
                    del in_to_out[inp]
                    del out_to_in[s]
                else:
                    inp.sendall(data)

# A továbbiakban a www. odaírása opcionális.

# Miért nem működik ez http-vel?
# proxy_destination = ("www.archlinux.org", 80)
# Futtatjuk -> böngészőben: localhost:8888
# 404 Not Found

# Észrevettük, hogy igazából ez https, úgyhogy írjuk át a portot 443-ra.
# proxy_destination = ("www.archlinux.org", 443)
# 400 Bad Request _ The plain HTTP request was sent to HTTPS port
# -> Mivel a localhost:9090 egy HTTP-s webcím, ezért a böngészőnk HTTP kérést
# -> küldött, és ezt próbáltuk proxy-zni egy HTTPS szerverre.
# -> Ez érthető módon nem működik.

# Próbáljuk ki a következővel is:
# proxy_destination = ("www.web.mit.edu", 80)
# Invalid URL _ The requested URL "[no URL]", is invalid.
# Mi a probléma?
# A Host: localhost:8888
# -> Amikor az MIT szervere olyat lát a kérésben, hogy "localhost:8888"
# -> és ez a 80-as portjára érkezett, akkor panaszkodni fog.
# -> Ugyanis a legtöbb szerver nem szereti, ha őt localhost-ként becézgetik.
# -> (HTTP kérést a böngésző a proxynknak küldi el, ezért van a proxynk a host mezőben.)
# -> A továbbított üzenet tartalmazott információt a címzettről (keresendő szerver neve, használt portja).
# -> MEGOLDÁS: simple_http_proxy.py
