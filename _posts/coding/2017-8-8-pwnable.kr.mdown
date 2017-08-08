---
layout:     post
title:      Pwnable.kr
category: coding
description: pwnable.kr Writeup
---

## 0x00 fd
Text： Mommy! what is a file descriptor in Linux?

![1](/pwnable-kr/1.jpg)

先ls看下都有什么文件，可以看到一个二进制文件，一份源码，和我们要拿到的flag

![2](/pwnable-kr/2.jpg)

看看源码，可以看出关键点就在于read函数，我对标准库也不是很了解所以想要找一份源码看看，但是并没有找到，根据查到零散资料我一开始把read函数理解为了从fd指向的内存中读取32字节到buf中，算好了 "LETMEWIN\n" 字符串的地址计算后的结果输入之后并没有成功。而fd的实际含义是linux对文件的一个索引id，而 `fd==0` 代表的含义是从终端中读取用户输入，所以我们只需要令 fd 为0就可以控制输入内容了。

附：[File Descriptor详解](http://blog.csdn.net/jnu_simba/article/details/8806654)