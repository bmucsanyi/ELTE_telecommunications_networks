from subprocess import PIPE, Popen
from time import sleep
cmd = ["timeout"]

processes = []
for i in range(4):
    p = Popen(cmd + ['/t', str(2 + i * 2), '/nobreak'], shell=True, stdout=PIPE, stderr=PIPE)
    processes.append(p)

empty_pool = False
done = []
while not empty_pool:
    run_counter = 0
    for p in processes:
        if p.poll() == None:  # Ha még nem ért véget
            run_counter += 1
        elif p not in done:  # Ha már véget ért, de még nem kezeltük le
            print(p.communicate()[0].decode('utf-8'))
            done.append(p)
    if run_counter > 0:
        print(f"{run_counter} subprocesses are still running...")
        sleep(1)
    else:
        empty_pool= True
        
print(processes)
