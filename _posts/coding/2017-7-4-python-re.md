---
layout: post
title: Python正则表达式
category: coding
description: Python正则表达式re模块介绍
---

0x00 正则表达式简介

正则表达式是对字符串进行操作的一种逻辑公式，是用预先定义好的一些特定的字符组合组成一个"规则"字符串，来对目标字符串进行匹配、过滤。在编程过程中有广泛应用，python有内建的re模块提供正则表达式的功能。

这里直接引用[百度百科](http://baike.baidu.com/item/正则表达式#4)对正则表达式中的通用符号进行说明。

0x01 re模块属性和方法

flags：

* re.A / re.ASCII - 表示仅匹配ASCII中的可见字符，不包括Unicode中其他内容

* re.I / re.IGNORECASE - 表示忽略大小写匹配

* re.L / re.LOCALE - 表示以当前区域设定编码匹配，注：自3.6版本开始与re.ASCII不兼容

* re.DEBUG - 在使用re.compile编译表达式时会显示调试信息

* re.M / re.MULTILINE - 这个标识会使'^'和'$'在每一行的开始和结束单独匹配，而不是在字符串的开始和结束匹配

* re.S / re.DOTALL - 表示'.'会匹配包括换行符在内的所有字符，默认情况下是不包括换行符的

* re.X / re.VERBOSE - 这个模式允许你为表达式添加注释，使其更加可读，该模式忽略空格，如需表示空格需要转义

methods:

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

* re.findall(*pattern, string, flags=0*)

** TO BE CONTINUED **