def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


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