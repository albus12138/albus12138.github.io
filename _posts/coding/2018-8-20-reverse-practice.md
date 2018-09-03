---
layout: post
title: 逆向练习
category: coding
description: 逆向练习 hackme.inndy.tw
---

## 0x00 helloworld

- 题目文件: [helloworld](../../images/inndy/helloworld)

- 分值: 40 pts

- FLAG{PI is not a rational number.}

从 main 函数中可以直接找到 magic number = 314159265, 可以直接将 magic number 输入到程序, 获取 flag, 也可以将 main 函数中的 flag 密文与 magic number 异或同样可以计算出flag

## 0x01 simple

- 题目文件: [simple-rev](../../images/inndy/simple-rev)

- 分值: 90 pts

- FLAG{THIS-IS-YOUR-FLAG}

从 main 函数中得到密文 `UIJT.JT.ZPVS.GMBH`, 然后逐位将 ASCII 码减一, 得到明文 THIS-IS-YOUR-FLAG, 加上格式即为答案

## 0x02 pyyy

- 题目文件: [pyyy.pyc](../../images/inndy/pyyy.pyc)

- 分值: 110 pts

- FLAG{VBXDVV4jkVVS4hVVj7NVV1heVVX1jVVh}

- [exp_pyyy.py](../../images/inndy/exp_pyyy.py)

通过 uncompyle6 将 pyc 文件反编译, 通过源码看出程序读取用户输入然后与计算值比较, 所以可以把比较部分删去, 直接运行, 得到flag

## 0x03 accumulator

- 题目文件: [accumulator](../../images/inndy/accumulator)

- 分值: 120 pts

- FLAG{051339467306f9769350136b41c330840eebcac337f1b8b0dc03e58be14fe690b123f61b0c0b35fc93ccc72100459369ef8531a1e8a7b4299e7b9d970b9a23aa}

- [exp_accumulator.py](../../images/inndy/exp_accumulator.py)


关键检验代码在 `sub_4008C0` 中, 是将输入的 flag 逐位累加, 然后与 0x601080 处的数据相比较, 所以在解密时可以通过 0x601080 处数据逐位减前一位内容得到每一位 flag

## 0x04 GCCC

- 题目文件: [gccc](../../images/inndy/gccc.exe)

- 分值: 140 pts

- FLAG{DO YOU KNOW GRAY CODE QAQQ}

- [exp_gccc.py](../../images/inndy/exp_gccc.py)

题目是用 .Net 写的, 可以用 dotPeek 反编译出源码, 可以看出只是一个异或移位的算法, 写出逆算法, 得到 flag

## 0x05 ccc

- 题目文件: [ccc](../../images/inndy/ccc)

- 分值: 150 pts

- FLAG{CRC32 is fun, but brute force is not}

- [exp_ccc.py](../../images/inndy/exp_ccc.py)

从 verify 中可以看出, flag 长度为 42, 每次取3位计算 CRC32, 然后与 hashes 中的值对比, 因此, 可以逐位爆破 CRC32 值

## 0x06 bitx

- 题目文件: [bitx](../../images/inndy/bitx)

- 分值: 150 pts

- FLAG{Swap two bits is easy 0xaa with 0x55}

- [exp_bitx.py](../../images/inndy/exp_bitx.py)

验证算法在 verify 中, 实质是交换奇偶位, 也可以当做一般算法写出逆算法

## 0x07 2018-rev

- 题目文件: [2018-rev](../../images/inndy/2018.rev)

- 分值: 150 pts

- FLAG{Happy New Year 2018, Keep Hacking Every Day!}

根据题目描述, 要求在 2018年1月1日 00:00:00 运行, 可以通过 ida 的动态调试, 下断点, 在程序获取本地时间之后进行修改, 也可以修改本地时间, 对于 flag 的计算, 是通过从 0x6CDE20 开始的 50 个字节解密的, 前 48 位被分为 6 个 QWORD 分别计算, 通过修改时间和启动参数可以获得 4 个正确值, 以此得到大部分 flag, 最后两个的值并没有看懂生成过程, 但根据解出的大部分 flag 猜出了剩余的内容 Orz

## 0x08 what-the-hell

- 题目文件: [what-the-hell](../../images/inndy/what-the-hell)

- 分值: 190 pts

- FLAG{modules inverse can help you..}

- [exp_what_the_hell.py](../../images/inndy/exp_what_the_hell.py)

这道题目的解密过程分为 2 步, 第一步是将输入的key与一些限定条件进行比较, 其中有两个等式, 要求其中一个为质数且是斐波那契数列中的一个值, 这一步可以通过 z3 求解器求出, 注意数据类型的长度, 存在溢出情况, 此外部分条件存在多解, 只有一个解可以满足所有条件, 得到正确的 key 之后就可以通过 junk_data 解密flag

## 0x09 unpackme

- 题目文件: [unpackme.exe](../../images/inndy/unpackme.exe)

- 分值: 200 pts

- FLAG{H0w dO yOU 7urn th1s 0n???}

- [exp_unpackme.py](../../images/inndy/unpackme.exe)

这道题从文件名就可以看出是个加了壳的题, 用 exeinfo 检测说是修改过的 upx 壳, 用 upx 直接脱失败, 然后是用 esp 定律手动脱壳, 应该是我技术的问题吧, 之前也没怎么练过手动脱壳, 脱出来的文件不能执行, 好在可以用ida分析了, 然后通过字符串搜索找到关键函数 sub_40BBB0, 首先是用 CSP 做了加密, 搜加密 id 0x8003 发现是 md5, 可以看出是以 md5 值与密文以及输入字符串的第一个字符循环异或得到flag, 这里有个问题就是通过 md5 查明文, 从 [cmd5](http://www.cmd5.com/) 查到了一个收费记录, 然后在 [somd5](https://www.somd5.com/) 查到了明文, 但是计算明文md5和给出的并不一致, 又去 [CrackStation](https://crackstation.net/) 查到了明文记录, 发现 somd5 没有显示完全, 缺少了最后几位...

## 0x0A mov

- 题目文件: [mov](../../images/inndy/mov)

- 分值: 200 pts

- FLAG{M0VFuscAtoR_15_ann0ying}

- [exp_mov.py](../../images/inndy/exp_mov.py)

之前已经见过几次 movfuscator, 每次都觉得能不能做出来全看玄学, 或者硬肛汇编, 我的汇编水平还不足以支撑我硬肛 Orz 拿到题目看到是 movfuscator 混淆之后首先试了一下有没有正确flag输出, 发现并没有, 然后用 intel pin 插桩计算指令数, 发现执行指令数收到是否正确以及长度影响, 然后在试的过程中发现了程序并不检测flag长度, 可以通过这样爆破

## 0x0B a-maze

- 题目文件: [maze.zip](../../images/inndy/maze.zip)

- 分值: 200 pts

- FLAG{W41k 410n3 1n m4z3 15 d4ng3r0u5, y0u m1gh7 n07 f1nd w4y r3v3r53}

- [exp_maze.py](../../images/inndy/exp_maze.py)

flag的检验算法很简单, 但是似乎并不好写逆向算法, 并且存在多条分支, 所以采用了递归的方式, 成功解出flag

## 这几天做了这几道题, 集中更新一下wp, 后续还会更新做题进度, 最后更新 8.28

