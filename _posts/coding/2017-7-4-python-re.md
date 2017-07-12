---
layout: post
title: Python正则表达式
category: coding
description: Python正则表达式re模块介绍
---

## 0x00 正则表达式简介

正则表达式是对字符串进行操作的一种逻辑公式，是用预先定义好的一些特定的字符组合组成一个"规则"字符串，来对目标字符串进行匹配、过滤。在编程过程中有广泛应用，python有内建的re模块提供正则表达式的功能。

这里直接引用[百度百科](http://baike.baidu.com/item/正则表达式#4)对正则表达式中的通用符号进行说明。

## 0x01 re模块属性和方法

**flags：**

* re.A / re.ASCII - 表示仅匹配ASCII中的可见字符，不包括Unicode中其他内容

* re.I / re.IGNORECASE - 表示忽略大小写匹配

* re.L / re.LOCALE - 表示以当前区域设定编码匹配，注：自3.6版本开始与re.ASCII不兼容

* re.DEBUG - 在使用re.compile编译表达式时会显示调试信息

* re.M / re.MULTILINE - 这个标识会使'^'和'$'在每一行的开始和结束单独匹配，而不是在字符串的开始和结束匹配

* re.S / re.DOTALL - 表示'.'会匹配包括换行符在内的所有字符，默认情况下是不包括换行符的

* re.X / re.VERBOSE - 这个模式允许你为表达式添加注释，使其更加可读，该模式忽略空格，如需表示空格需要转义

**methods:**

* re.search(*pattern, string, flags=0*) - 返回匹配到的第一个对象，如果没有任何匹配，返回 `None`

* re.match(*pattern, string, flags=0*) - 如果字符串开头的字符满足表达式，则返回一个对象，否则，返回 `None` ，注意，re.MULTILINE在此函数中不起作用

* re.fullmatch(*pattern, string, flags=0*) - 如果整个字符串匹配表达式，则返回一个对象，否则，返回 `None`，注：自3.4版本添加

* re.split(*pattern, string, maxsplit=0, flags=0*)
{% highlight python %}
re.split('\W+', 'Words, words, words.')
# ['Words', 'words', 'words', '']

# 加括号后会将为匹配字符都加入列表中
re.split('(\W+)', 'Words, words, words.')
# ['Words', ', ', 'words', ', ', 'words', '.', '']

# maxsplit如果不为0则只截取出规定个数的子串
re.split('\W+', 'Words, words, words.', 1)
# ['Words', 'words, words.']
{% endhighlight %}
注意：自3.1版本起支持flags，自3.5版本起不接受空正则表达式，如：`"^$"`

* re.findall(*pattern, string, flags=0*) - 返回一个列表，其中是字符串所有不重叠的子串，当没有任何匹配时，返回一个空列表

* re.finditer(*pattern, string, flags=0*) - 返回一个结果列表的迭代器

* re.sub(*pattern, repl, string, count=0, flags=0*) - 将string中符合pattern匹配的子串用repl替换，返回替换后的字符串，这里的repl可以是字符串，也可以是函数，如果是函数，匹配到的子串会作为参数传入函数

* re.escape(pattern) - 对pattern中的一些特殊字符进行转义，使其满足正则表达式的要求

* re.purge() - 清除之前缓存中的正则表达式

0x02 返回对象的属性和方法

* obj.expand(template) - 通过反斜杠+数字 `\1` 或为反斜杠命名 `\g<name>` 来标记要替换子串的位置，功能相当于 sub 函数

* obj.group([group1, ...]) - 返回一个包含结果的元组，如果参数为0或空，则返回全部结果，其他情况下返回对应的结果

* obj.groups(default=None) - 返回一个元组，包含所有匹配到的子串，若没有匹配到则为default的值

* obj.groupdict(default=None) - 返回一个字典，其中key是正则中的命名，value为匹配到的值

* obj.start() / obj.end() - 这个匹配对象在原字符串中的起/止位置

* obj.span() - 以元组的形式返回子串的起止位置 `(start, end)`

* obj.pos / obj.endpos - 传给re.match() / re.search() 的 pos / endpos 参数

* obj.re - 匹配这个对象的正则表达式对象

* obj.re - 匹配这个对象的字符串对象

最后附上[官方文档](https://docs.python.org/3/library/re.html)