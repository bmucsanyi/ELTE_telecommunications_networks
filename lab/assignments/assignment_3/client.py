import argparse
import random
import socket
import struct
import sys
import time


NUM_RANGE = (1, 100)


def create_guess_struct(comp, num):
    return struct.pack('ci', comp, num)


def get_result_from_struct(struct_):
    # we throw away the number, as we only care about the char
    return struct.unpack('ci', struct_)


def recvall(sock, length):
    return sock.recv(length, socket.MSG_WAITALL)


def step_guess(current_range):
    if current_range[1] - current_range[0] == 1:
        # we have only one choice
        current_guess = current_range[0] 
        return create_guess_struct(b'=', current_guess)
    else:
        current_guess = (current_range[0] + current_range[1]) // 2
        return create_guess_struct(b'<', current_guess)


def step_range(result, current_range, current_number):
    if result == 'I':
        current_range[1] = current_number
    elif result  == 'N':
        current_range[0] = current_number
    else:
        raise ValueError('Invalid response received.')


def is_over(result):
    return result in ('K', 'Y', 'V')


def play_game(args, verbose=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # contextmanager doesn't save us from KeyboardInterrupt
        # (and GeneratorExit)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.connect((args.bind_address, args.bind_port))

        current_range = list(NUM_RANGE)

        running = True
        while running:
            guess_bytes = step_guess(current_range)
            
            time.sleep(random.randint(1, 5))
            client.sendall(guess_bytes)

            response = recvall(client, 8)
            result = get_result_from_struct(response)[0].decode()

            guess = get_result_from_struct(guess_bytes)
            current_number = int(guess[1])

            if verbose:
                print(f">>> {guess[0].decode()} {guess[1]}")
                print(f"<<< {result}")

            if is_over(result):
                return

            step_range(result, current_range, current_number)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bind_address', type=str)
    parser.add_argument('bind_port', type=int)
    args = parser.parse_args(sys.argv[1:])

    play_game(args, verbose=True)


if __name__ == "__main__":
    main()