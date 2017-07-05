---
layout: post
title: XCTF嘉年华体验赛 Re部分WriteUp
category: coding
description: XCTF嘉年华体验赛 RE题解
---
## 0x00 Re1

题目比较简单，用IDA反编译出伪代码

![main](/images/xctf-carnival-wp/1.jpg)

可以看出，flag是一个4位纯数字字符串`abcd`，其中可以从if条件得出4个限制条件，相当于解一个四元一次方程组

* a+b+c+d = 23

* c div d = 2

* b-c = 1

* a mod c = 3

不难算出结果，flag：9563

不想动笔算的话就写个爆破脚本好了

{% highlight python linenos %}
for a in range(0, 10):
    for b in range(0, 10):
        for c in range(0, 10):
            for d in range(0, 10):
                if a+b+c+d != 23:
                    continue
                if d == 0 or c == 0:  # 除数不能为0
                    continue
                if divmod(c, d)[0] != 2:
                    continue
                if b != c - 1:
                    continue
                if divmod(a, c)[1] != 3:
                    continue
                print a, b, c, d
{% endhighlight %}

## 0x01 Re2

这是AlexCTF的一道原题，用IDA生成伪代码后先看看main函数

![main](/images/xctf-carnival-wp/2.jpg)

题目设置了两个非常长的sleep，很不友好，需要破解的内容分别是username和password，不难看出一共涉及到了5个函数

*sub_400C9A*:

![400C9A](/images/xctf-carnival-wp/3.jpg)

一个获取字符串长度的函数，并将长度传入`sub_400C41`进一步运算

*sub_400C41*:

![400C41](/images/xctf-carnival-wp/4.jpg)

通过四个条件限制字符串长度，因为涉及到了unsigned int，这里选择用c++写爆破脚本，得出结果，username长度为8或12

{% highlight C++ linenos %}
#include <iostream>
using namespace std;

int main(){
	unsigned int result;
	for(int i=0; i<49; ++i){
		result = i>>3;
		if(4*(i>>2)!=i || 4*(i>>4)!=i>>2 || !result || i>>4){}
		else{
			cout << i << endl;
		}
	}
}
{% endhighlight %}

*sub_400CDD*:

![400CDD](/images/xctf-carnival-wp/5.jpg)

DWORD是双字类型，长度为4字节，这里用DWORD从字符串中截取出4个字符，也就是分段检验，通过if的条件不难算出v2、v3、v4的值，转换为hex即为username字符串。这里要注意一点，IntelCPU采用的是小端序，所以存储的值与实际的值是相反的，需要对解出的4位字符串进行反转。

*sub_4008F7*:

![4008F7](/images/xctf-carnival-wp/6.jpg)

这个函数对username进行了逐位检验，允许的字符为小写字母和_，其实上一个函数中已经解出正确的username，这里检验意义不大

*sub_400977*:

![400977](/images/xctf-carnival-wp/7.jpg)
![400977](/images/xctf-carnival-wp/8.jpg)

首先是对字符进行检验，允许的字符为大小写字母和数字，然后同样是一个分段检验，这里用到一个伪随机，种子为打乱顺序的之前解出的username，写一个c++脚本输出一下伪随机的前十个值，与对应结果进行运算，即可得到password。

{% highlight C++ linenos %}
#include <iostream>
#include <stdlib.h>
using namespace std;

int main(){
	srand(0x454D3E2E);
	for(int i = 0; i < 10; i++){
		cout << rand() << endl;
	}
}
{% endhighlight %}

*sub_400876*:

![400876](/images/xctf-carnival-wp/9.jpg)

这里其实是一个输出正确flag的函数，这里的字符串s不知道在哪里，是不是与username和password有关，一开始也想过直接解开这个函数得到flag，但是没有思路，最后也没有逆向这个函数。

将上面算出的username和password写入程序中，经过漫长的等待（这里画个圈圈诅咒出题人），得到答案 your flag is: ALEXCTF{1_t41d_y0u_y0u_ar3__gr34t__reverser__s33}