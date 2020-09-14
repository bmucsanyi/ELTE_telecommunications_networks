from subprocess import PIPE, Popen
from time import sleep
cmd = ["timeout", "/t", "30", "/nobreak"]

process = []
for i in range(4):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    process.append(p)

for p in process:
    p.wait()

for p in process:
    print(p.communicate()[0].decode('utf-8'))

print("kész")