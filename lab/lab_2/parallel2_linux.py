from subprocess import PIPE, Popen
from time import sleep


def main():
    cmd = ["sleep", "5"]

    process = []
    for i in range(4):
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        process.append(p)

    for p in process:
        p.wait()

    for p in process:
        print(p.communicate()[0].decode('utf-8'))

    print("Finished")


if __name__ == "__main__":
    main()