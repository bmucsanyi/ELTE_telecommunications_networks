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
            if len(data) == 0:
                break
            elif len(data) > 0 and data[-1] == 0:
                break
            elif len(data) > 3 and data[-4:] == "\r\n\r\n".encode():
                break
            elif len(data) > 1 and data[-2:] == "\n\n".encode():
                break
        req = req.decode()
        req = req.replace("localhost:" + str(sys.argv[1]), sys.argv[2])
        req = req.replace("localhost", sys.argv[2])
        print(req)
        # keep = "keep-alive" in req

        proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_sock.connect((sys.argv[2], int(sys.argv[3])))
        proxy_sock.sendall(req.encode())
        proxy_sock.settimeout(0.1)  # win-hez

        while True:
            data = proxy_sock.recv(1024)
            # print(data)
            client_socket.send(data)
            if len(data) == 0:
                break
        proxy_sock.close()
    except Exception as e:
        print(e)
    client_socket.close()


# Ugyanúgy van egy socket-ünk, amin várjuk a kérést.
# (Egyszerűság kedvéért nem selectes megoldás.)
# Egészen addig várunk, amíg a dupla enter ott nincs az üzenet végén
# (Ez a HTTP kérés lezárása.)
# Ekkor a HTTP kérésben kicseréljük a localhostot arra, ami valóban a cél (proxyzott szerver).
# pl.: python simple_http_proxy.py 9090 web.mit.edu 80
# -> Ha nincs átirányítás vagy teljes URL megadva, akkor tökéletesen tudunk linkeken haladva
# -> továbbra is a proxyn keresztül böngészni.

# Miért jó a proxy?
# Ülünk a koliban, kolinet rossz, nem jön be semmi.
# Rájövünk, hogy az ELTE-s szervereket nagyon jól el tudjuk érni,
# tehát nem a kollégium kijárója van leterhelve, hanem
# az egyetem általános, tanulóknak fenntartott kijárója.
# Ha be SSH-zunk egy ELTE-s projektszerverre, aminek van direkt internetkapcsolata
# kifelé is, azt pl. tudjuk használni, gyors lesz a net.

# inf.elte.hu-val nem fog működni a proxynk 443-as porton,
# a tcp_proxy.py-ban leírtak miatt.
# -> Írjunk akkor a böngészőnkbe https://localhost:9090-et!
# -> A biztonságos kapcsolat sikertelen!
# -> A HTTPS-t nem csak arra használják, hogy a kommunikáció
# -> titkos legyen, hanem hogy megfelelően azonosítható legyen a szerver.
# -> Senki se fogja az én localhostomra azt mondani, hogy ez az eltének a címe.
# -> Nem lehet olyan triviálisan ezt kiaknázni, hogy a localhostot kicserélem
# -> a kérésben.