import struct
import zlib

data = b"\x6F\x59\x41\xD6\x90\xE9\xA3\x80\x9B\x5C\x8D\xC9\xAF\xAF\x05\x0D\x2D\xA1\x72\x13\x7B\x11\x5F\x5D\xFD\xFB\x01\x40\x6B\xD5\xD2\xA7\x7E\xFB\x04\x7D\x5E\x89\x42\x2E\xB3\x7E\xC9\x61\xC3\x43\xAB\x84\xDD\x29\xC1\x9F\x4D\x2F\x59\xF4"

udata = struct.unpack("<"+"I"*14, data)

def process(base, index):
    if index == 14:
        print(base)
        return 0
    for i in range(32, 128):
        for j in range(32, 128):
            for k in range(32, 128):
                s = base + chr(i) + chr(j) + chr(k)
                if zlib.crc32(s.encode("utf8")) == udata[index]:
                    print(s)
                    process(s, index+1)
                    return 0

process("", 0)
