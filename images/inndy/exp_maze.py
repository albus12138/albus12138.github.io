import sys
import struct

with open("map", "rb") as rfile:
    map_data = rfile.read()

v2 = -1
data = struct.unpack("<514048i", map_data)


def process(v2, flag):
    if v2 == 0:
        print(flag)
        sys.exit(0)
    for j in range(32, 128):
        ch = chr(j)
        for i in range(0, len(data)):
            if data[i] == v2 and (i * 4 - 4 * ord(ch)) % 512 == 0:
                flag = ch + flag
                v2 = int((i * 4 - 4 * ord(ch)) / 512)
                print(i, int((i * 4 - 4 * ord(ch)) / 512), flag)
                process(v2, flag)


process(-1, "")