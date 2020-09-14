import sys


def is_leap_year(year):
    return (year % 4 == 0 and not year % 100 == 0) or year % 400 == 0


def main():
    with open(sys.argv[1]) as f:
        for year in f:
            int_year = int(year)
            print(f"{int_year} is {'not ' if not is_leap_year(int_year) else ''}a leap year")


if __name__ == "__main__":
    main()