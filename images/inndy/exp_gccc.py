num_list = [164, 25, 4, 130, 126, 158, 91, 199, 173, 252, 239, 143, 150, 251, 126, 39, 104, 104, 146, 208, 249, 9, 219, 208, 101, 182, 62, 92, 6, 27, 5, 46]

num = 0

for i in num_list:
    num = num ^ i

str2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{} "

def check(result, index, num):
    c = num_list[index] ^ result ^ num
    c = c & 0xff
    if index == 0 and chr(c) != "F":
        return False
    if index == 1 and chr(c) != "L":
        return False
    if index == 2 and chr(c) != "A":
        return False
    if index == 3 and chr(c) != "G":
        return False
    if index == 4 and chr(c) != "{":
        return False
    if index == 31 and chr(c) != "}":
        return False
    if chr(c) not in str2:
        return False
    return True

def process(result, index, num):
    if index < 0:
        calc(result)
        return 0
    num ^= num_list[index]
    if check(int(result+"0", 2), index, num):
        process(result+"0", index-1, num)
    if check(int(result+"1", 2), index, num):
        process(result+"1", index-1, num)

def calc(key):
    key = int(key, 2)
    num = 0
    str1 = ""
    index = 0
    while key != 0:
        c = chr(num_list[index] ^ key & 0xff ^ num & 0xff)
        str1 += c
        num ^= num_list[index]
        index += 1
        key = key >> 1
    print(str1)

process("", 31, num)

