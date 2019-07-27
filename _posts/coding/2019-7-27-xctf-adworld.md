2019-7-27-xctf-adworld

---
layout: post
title: XCTF攻防世界writeup
category: coding
description: XCTF攻防世界writeup
---

## Reverse

### 0x00 re1

- flag: DUTCTF{We1c0met0DUTCTF}

`_mm_storeu_si128((__m128i *)&v5, _mm_loadu_si128((const __m128i *)&xmmword_413E34));`将flag加载到v5中，与输入比较，相同则输出flag

### 0x01 game

- flag: zsctf{T9is_tOpic_1s_v5ry_int7resting_b6t_others_are_n0t}

从字符串 `done!!! the flag is ` 定位到关键函数，v2[i]^v2[i+68]^0x13即为flag

### 0x02 helloctf

- flag: CrackMeJustForFun

main函数中包含hex字符串 `437261636b4d654a757374466f7246756e` 解码得到flag

### 0x03 code

- flag: c0ffee

要求带3个参数运行，第一个参数为0xcafe，第二个参数模17余8且模5不余3，第三个参数为h4cky0u

### 0x04 simple-unpack

- flag: flag{Upx_1s_n0t_a_d3liv3r_c0mp4ny}

upx壳，直接 `upx -d`，main函数明文flag

### 0x05 insanity

- flag: 9447{This_is_a_flag}

随机输出字符串

### 0x06 logmein

- flag: RC3-2016-XORISGUD

循环异或，密文 `:\"AL_RT^L*.?+6/46` 密钥 `harambe`

### 0x07 no-strings-attached

- flag: 9447{you_are_an_international_mystery}

decrypt之后下断点，locals读取变量s2

### 0x08 python-trade

- flag: nctf{d3c0mpil1n9_PyC}

pyc反编译，先base64解码，逐位减16异或32

### 0x09 csaw2013reversing2

- flag: flag{reversing_is_not_that_hard!}

- [fs寄存器信息](https://en.wikipedia.org/wiki/Win32_Thread_Information_Block)

题目中有检测调试器，在检测到调试器后执行解码后直接退出，没检测到调试器则不解码输出，所以nop掉退出代码，用调试器运行直接获得flag

### 0x10 getit

- flag: SharifCTF{b70c59275fcfa8aebf2d5911223c6589}

密文 `b70c59275fcfa8aebf2d5911223c6589` 奇数位+1 偶数位-1

### 0x11 maze

- flag: nctf{o0oo00O000oooo..OO}

走迷宫，从字符串常量里找到迷宫地图，从(0, 0)出发，走到#位置，路线即为flag