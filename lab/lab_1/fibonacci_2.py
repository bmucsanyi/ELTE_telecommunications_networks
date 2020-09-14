def fibonacci_list(n):
    ret = [0, 1]
    if n == 0:
        return ret[:-1]
    while len(ret) < n:
        ret.append(ret[-1] + ret[-2])
    return ret


def fibonacci(n):
    a, b = 0, 1
    if n == 0:
        return a
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def main():
    print("Get the nth element of the Fibonacci sequence (quit: q)")
    while True:
        print(">>> ", end='')
        n = input()
        if n == "q":
            break
        else:
            try:
                n = int(n)
                print(f"Fibonacci_n = {fibonacci(n)}")
            except ValueError:
                print("Invalid number!")


if __name__ == "__main__":
    main()