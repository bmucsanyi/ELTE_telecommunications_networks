import subprocess


def main():
    print("~~~~~~~~~~~~~~~~~~~~")
    # Old interface:
    # If we provide a list and shell=True, it only calls the cmd with the first
    # argument, and gives the others to the shell (thus ignoring it in this case),
    # so when we call with shell=True (which we shouldn't do by the way), we
    # should only provide a list with a single argument containing all the
    # switches, too.
    returncode = subprocess.call(["ls", "-l"])
    print(returncode)
    # New interface:
    result = subprocess.run(["ls", "-l"])
    print(result.returncode)
    input()

    print("~~~~~~~~~~~~~~~~~~~~")
    p = subprocess.Popen(["echo", "Hello world"], stdout=subprocess.PIPE)
    print(p.communicate()[0].decode("utf-8"))
    input()

    print("~~~~~~~~~~~~~~~~~~~~")
    p1 = subprocess.Popen(["find"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", ".py"], stdin=p1.stdout, stdout=subprocess.PIPE)

    print(p2.communicate()[0].decode("utf-8"))


if __name__ == "__main__":
    main()