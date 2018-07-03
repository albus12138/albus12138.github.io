---
layout: post
title: Fluent Python笔记
category: coding
description: Fluent Python 内容小结
---

## Part 1: 序言

### Chapter 1 | Python数据模型

- `magic method` 是一种特殊的方法,形式如 `__getitem__`,可以让我们自定义的类具有一些原生类的效果,如 `len(obj)` 就是调用对象的 `__len__` 方法,如果我们自定义的类实现了这个方法,就可以通过 `len` 获得长度 [更多内容](https://docs.python.org/3/reference/datamodel.html#special-method-names)

## Part 2: 数据结构

### Chapter 2 | 序列

- 分类
	- Container(容器) sequences & Flat(平坦) sequences
		- list, tuple, collections.deque(Double-End Queue)
		- str, bytes, bytearray, memoryview, array.array

	- Mutable(可修改) sequences & Immutable(不可修改) sequences
		- list, bytearray, memoryview, array.array, collections.deque
		- tuple, str, bytes

- 递推式构造列表 (List Comprehensions and Generator Expressions)
	- `[ord(x) for x in "ABC" if ord(x) < ord('C')]` => `[65, 66]`
	- 通过这样的方式构建列表相比于循环或是map更具有可读性 [执行效率测试](https://github.com/fluentpython/example-code/blob/master/02-array-seq/listcomp_speed.py)
	- __注意__:在Python 3.x以前,这个表达式会导致内部循环变量泄露,如果在外部有同名符号会被覆盖

- 解包 (Unpacking)
	- 元组: `latitude, longitude = (33.9425, -118.408056)`
	- 处理多余元素: `a, *b, c = range(5)` => `a = 0, b = [1, 2, 3], c = 4`
	- 嵌套元组: `name, cc, pop, (latitude, longitude) = ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))`
	- 命名元组:
	{% highlight python %}
	from collections import namedtuple
	City = namedtuple('City', 'name country population coordinates')
	tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
	# >>> tokyo
	# City(name='Tokyo', country='JP', population=36.933, coordinates=(35.689722, 139.691667))
	# >>> tokyo.population
	# 36.933
	# >>> tokyo[1]
	# 'JP'
	{% endhighlight %}

- 切片对象 (Slice objects)
	- `s[a:b:c]` 从a到b步长为c
	- `slice(start, stop[, step])` 生成一个切片对象,使用方法 `s[sliceObj]`
	- 多维切片 `a[m:n, i:j]` `a[i, :, :,]` [更多内容](http://scipy.github.io/old-wiki/pages/Tentative_NumPy_Tutorial)
	- 使用切片对象修改可修改序列
	{% highlight python %}
	l = list(range(10))
	# l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	l[2:5] = [20, 30]
	# l = [0, 1, 20, 30, 5, 6, 7, 8, 9] 不足的元素会被删除
	del l[5:7]
	# l = [0, 1, 20 ,30, 5, 8, 9]
	# l[2:5] = 100 错误!
	l[2:5] = [100]
	# l = [0, 1, 100, 8, 9]
	{% endhighlight %}
	
- 构建嵌套列表
	- `[['_'] * 3 for i in range(3)]` => `[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]`

- +=问题
	- `t = (1, 2, [10, 20]); t[2] += [30, 40]` 会引发一个TypeError,但t的值仍会被修改
	- 所以,在不可变序列中放入一个可变类型是一个不明智的选择

<strong>To be Continued...</strong>