import random
import socket


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        tcp.connect(('localhost', 11111))  # 11111 is the history server

        money = input('> ')
        try:
            int(money)
        except ValueError:
            print('invalid amount of money')

        num_list = [str(random.randint(1, 20)) for _ in range(5)] + [money]
        data = ':'.join(num_list).encode()

        tcp.sendall(data)

        resp = tcp.recv(256)
        resp = resp.decode().split(':')
        prize = int(resp[-1])
        winner_numbers = [int(num) for num in resp[:-1]]

        print(f'You won {prize} dollars.')
        print('The winner numbers were', winner_numbers)


if __name__ == "__main__":
    main()