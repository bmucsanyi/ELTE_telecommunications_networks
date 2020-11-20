import subprocess


def main():
    print("~~~~~~~~~~~~~~~~~~~~")
    # Old interface:
    returncode = subprocess.call(["dir", "/B"], shell=True)
    print(returncode)
    # New interface:
    result = subprocess.run(["dir", "/B"], shell=True)
    print(result.returncode)

    # The only time you need to specify shell=True on Windows is when
    # the command you wish to execute is built into the shell (e.g. dir or copy).
    # You do not need shell=True to run a batch file or console-based executable.

    input()

    print("~~~~~~~~~~~~~~~~~~~~")
    p = subprocess.Popen(["echo", "Hello world"],
                         shell=True,
                         stdout=subprocess.PIPE)
    print(p.communicate()[0].decode("utf-8"))
    input()

    print("~~~~~~~~~~~~~~~~~~~~")
    p1 = subprocess.Popen(["dir", "d:\\", "/b"],
                          shell=True,
                          stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["find", '"V"'], shell=True, stdin=p1.stdout, stdout=subprocess.PIPE)

    print(p1.communicate()[0].decode("utf-8"))  # new line is \r\n
    print(p2.communicate()[0].decode("utf-8").split("\n"))  # Access denied, for some reason.


if __name__ == "__main__":
    main()