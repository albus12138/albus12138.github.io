from subprocess import Popen, PIPE
from string import printable

ans = "FLAG{"
while True:
    if "}" in ans:
        print(ans)
        break

    for c in printable:
        f = Popen("./mov", shell = True, stdin = PIPE, stdout = PIPE)
        tmp = ans + c
        tmpp = tmp + "\n"
        f.stdin.write(tmpp.encode("u8"))
        
        stdout, stderr = f.communicate()
        if "Good".encode("u8") in stdout:
            ans = tmp
            print(ans)
            break
