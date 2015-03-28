---
layout:     post
title:      缓冲区溢出攻击相关知识 
category: bookmarks
description: 缓冲区溢出攻击相关知识，Mark！
---


本文是coursera软件安全课程学习总结，算是梳理知识，细节太多，只写了要点。

##  内存模型

<img src="/images/buffer-overflow/1.png">

###  内存分配

使用malloc函数分配的内存在heap区域，stack从高地址向低地址生长，heap相反。

<img src="/images/buffer-overflow/2.png">

###  函数调用时的堆栈变化

每当使用call指令进行函数调用时，都会将原来的eip寄存器中的值压栈，然后，将新的函数指针写入eip寄存器，这是由机器自动执行的，保存原eip的同时，将新的执行地址写入eip.详细过程可以关注我的博客中一篇详细描述堆栈变化的博文click here。

这里我们知道，一旦函数调用完毕，返回地址如果被修改（比如被修改成为恶意程序的入口地址），那么后果不堪设想。使用缓冲区溢出可以实现攻击 ，我们会在例子中给出解释。

接下来我们使用一个例子来形象的表示出函数调用时堆栈的变化

{% highlight c %}
    void f(char* str,int i,int j){
        int local1;
        int local2;
        ...
    }
    int main(){
        ...
        f("tom",8,9);
        ...
    } 
{% endhighlight %}

<img src="/images/buffer-overflow/3.png">

##  代码注入

如何进行代码注入？首先，我们需要把代码放入内存。其次，需要让eip指向我们的代码起始位置，才能执行它。

### 将代码加载到内存

*   代码必须是已编译的可执行机器码

*   代码不能包括零，否则，零之后I/O函数将停止拷贝

*   不能使用loder

我们的目标是执行一个我们可以操纵的shell,加载shell的代码被称为shellcode。

{% highlight c %}
    #include <stdio.h>
    int main( ) {
       char  *name[2];
       name[0] = “/bin/sh”;
       name[1] = NULL;
       execve(name[0], name, NULL);
    }
{% endhighlight %}

###  让已经加载的代码运行起来

由于在函数调用的末尾，需要将原eip值取出加载到eip寄存器，那么，如果我们修改了原eip的值，使其变为我们shellcode代码执行地址，那么函数返回后就执行shellcode。

可是，怎么知道我们的shellcode指令开始地址呢？因为如果地址不正确，CPU就故障了。

如果我们没有权限获取代码，我们当让不知道缓冲区距离ebp有多远，那么，我们怎么办呢？

*   尝试！不停尝试（这个看运气，而且几率不高）
*   如果没有地址随机优化，那么每次堆栈都从一个固定的地址开始执行，而且堆栈一般不会很深，那么，可以知道esp大体在某个区间。可以使用 nop sleds 提高我们的命中几率。

nop sleds:

<img src="/images/buffer-overflow/4.png">

以上我们讨论的就是所谓的stack smashing。

##  其他内存攻击

###  堆溢出

把缓冲区溢出的原理用在堆上，就是所谓的堆溢出。

###  整数溢出

<img src="/images/buffer-overflow/5.png">

###  读溢出

读取了不该读取的内存

the Heartbleed bug 通过发送特定的消息，拥有bug的ssl服务器没有检查长度就将攻击者指定的返回字符串返回攻击者。因此，攻击者可以通过增大字符串长度，非法读取其他数据。

###  被释放的指针再次使用

##  格式化字符串攻击

###  正常情况下的printf函数

<img src="/images/buffer-overflow/6.png">

### 不安全时

<img src="/images/buffer-overflow/7.png">

读取了调用者的数据！

举例：

{% highlight c %}
    printf(“100% dave”);
    //Prints stack entry 4 byes above saved %eip 
    printf(“%s”); 
    //Prints bytes pointed to by that stack entry 
    printf(“%d %d %d %d …”);
    //Prints a series of stack entries as integers 
    printf(“%08x %08x %08x %08x …”);
    // Same, but nicely formatted hex 
    printf(“100% no way!”)"
    //WRITES the number 3 to address pointed to by stack entry
{% endhighlight %}

###  例子解释

{% highlight c %}
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <errno.h>
    #include <string.h>
    #include <sys/types.h>
    #include <time.h> 

    char greeting[] = "Hello there
    1. Receive wisdom
    2. Add wisdom
    Selection >";
    char prompt[] = "Enter some wisdom
    ";
    char pat[] = "Achievement unlocked!
    ";
    char secret[] = "secret key";

    int infd = 0; /* stdin */
    int outfd = 1; /* stdout */

    #define DATA_SIZE 128

    typedef struct _WisdomList {
      struct  _WisdomList *next;
      char    data[DATA_SIZE];
    } WisdomList; 

    struct _WisdomList  *head = NULL;

    typedef void (*fptr)(void);

    void write_secret(void) {
      write(outfd, secret, sizeof(secret));
      return;
    }

    void pat_on_back(void) {
      write(outfd, pat, sizeof(pat));
      return;
    }

    void get_wisdom(void) {
      char buf[] = "no wisdom
    ";
      if(head == NULL) {
        write(outfd, buf, sizeof(buf)-sizeof(char));
      } else {
        WisdomList  *l = head;
        while(l != NULL) {
          write(outfd, l->data, strlen(l->data));
          write(outfd, "
    ", 1);
          l = l->next;
        }
      }
      return;
    }

    void put_wisdom(void) {
      char  wis[DATA_SIZE] = {0}; 
      int   r;

      r = write(outfd, prompt, sizeof(prompt)-sizeof(char));
      if(r < 0) {
        return;
      }

      r = (int)gets(wis); 
      if (r == 0)
        return;

      WisdomList  *l = malloc(sizeof(WisdomList));

      if(l != NULL) {
        memset(l, 0, sizeof(WisdomList));
        strcpy(l->data, wis);
        if(head == NULL) {
          head = l;
        } else {
          WisdomList  *v = head;
          while(v->next != NULL) {
            v = v->next;
          }
          v->next = l;
        }
      }

      return;
    }

    fptr  ptrs[3] = { NULL, get_wisdom, put_wisdom };

    int main(int argc, char *argv[]) {

      while(1) {
          char  buf[1024] = {0};
          int r;
          fptr p = pat_on_back;
          r = write(outfd, greeting, sizeof(greeting)-sizeof(char));
          if(r < 0) {
            break;
          }
          r = read(infd, buf, sizeof(buf)-sizeof(char));
          if(r > 0) {
            buf[r] = "";
            int s = atoi(buf);
            fptr tmp = ptrs[s];
            tmp();
          } else {
            break;
          }
      }

      return 0;
    }
{% endhighlight %}

本实验所有材料来自coursera软件安全课程。

这个例子包含两个缓冲区溢出攻击。主函数中包含一个全局缓冲区攻击，函数put_wisdom中的wis缓冲区是一个栈上的缓冲区溢出。

执行过程：

*   编译程序，gcc -fno-stack-protector -ggdb -m32 wisdom-alt.c -o wisdom-alt
*   使用bash打开一个终端，运行./runbin.sh
*   打开另一个终端，使用命令 gdb -p `pgrep wisdom-alt`调试

<img src="/images/buffer-overflow/8.png">

###  ptrs输入超过2的索引出现错误

回想之前的缓冲区溢出，如果我们输入的索引值恰好能到达fptr p = pat_on_back;中p的存储区域，那么就能读取到pat_on_back，进而执行该函数！

首先，确定p的地址：在启动运行gdb中print &p和print buf:

<img src="/images/buffer-overflow/9.png">

通过计算，知道p在buf之前771675416个内存位置处，我们输入该数字：

<img src="/images/buffer-overflow/10.png">

发现我们获取到了到了pat_on_back函数指针！

###  void put_wisdom(void)函数中的栈上缓冲区溢出

同样的原理，我们通过找到函数void put_wisdom(void) 被调用时缓冲区wis的地址和返回地址在内存中的差，用同样的方法，将我们函数指针write_secret的地址写入保存返回地址的内存区域，那么函数put_wisdom调用结束后，就会执行write_secret函数。