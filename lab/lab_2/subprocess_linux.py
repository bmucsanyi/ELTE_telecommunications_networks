import subprocess

print("~~~~~~~~~~~~~~~~~~~~")
# Old interface:
returncode = subprocess.call(["ls", "-l"], shell=True)
print(returncode)
# New interface:
result = subprocess.run(["ls", "-l"], shell=True)
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