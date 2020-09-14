from subprocess import PIPE, Popen
from time import sleep
cmd = ["sleep"]

process = []
for i in range(4):
    p = Popen(cmd + [str(2+i*2)], stdout=PIPE, stderr=PIPE)
    process.append(p)

ures = False
done = []
while (not ures):
    fut = 0
    for p in process:
        if p.poll() == None:
            fut += 1
        elif p not in done:
            print(p.communicate())
            done.append(p)
    if (fut > 0):
        print("Meg futnak")
        sleep(1)
    else:
        ures = True
print("kész",process)