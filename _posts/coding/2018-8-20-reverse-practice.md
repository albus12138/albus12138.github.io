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


## 这几天做了这几道题, 集中更新一下wp, 后续还会更新做题进度

