import subprocess

print("~~~~~~~~~~~~~~~~~~~~")
subprocess.call(["ls","-l"])
input()

print("~~~~~~~~~~~~~~~~~~~~")
p = subprocess.Popen(["echo","Hello world"],stdout=subprocess.PIPE)
print(p.communicate())
input()

print("~~~~~~~~~~~~~~~~~~~~")
p1 = subprocess.Popen(["find"], stdout=subprocess.PIPE)
p2 = subprocess.Popen(["grep", ".py"], stdin=p1.stdout, stdout=subprocess.PIPE)

print(p2.communicate()[0].decode("utf-8").split("\n"))