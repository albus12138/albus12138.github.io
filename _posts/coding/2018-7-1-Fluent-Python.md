---
layout: post
title: Fluent Python笔记
category: coding
description: Fluent Python 内容小结
---

## Part 1: 序言

### Chapter 1 | 数据模型

- `magic method` 是一种特殊的方法,形式如 `__getitem__`,可以让我们自定义的类具有一些原生类的效果,如 `len(obj)` 就是调用对象的 `__len__` 方法,如果我们自定义的类实现了这个方法,就可以通过 `len` 获得长度 [更多内容](https://docs.python.org/3/reference/datamodel.html#special-method-names)

## Part 2: 数据结构

### Chapter 2 | 序列

- 分类
	- Container(容器) sequences & Flat(平坦) sequences
		- list, tuple, collections.deque(Double-Ended Queue)
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

- 排序
	- `obj.sort(key, reverse) or sorted(obj, key, reverse)` 其中 `sorted` 不改变原序列顺序
	- `reverse`为真时,将降序排列,key是一个单参数函数,通过该函数返回值排序
	- 二分查找 & 插入
		- 因为排序操作付出的代价是很高的,所以在排序后保持序列有序就十分重要
		- `bisect.bisect(haystack, needle)` 在 `haystack` 中查找探针应该插入的位置, 再通过 `haystack.insert(index, needle)` 将探针插入对应位置
		- `bisect.indort(haystack, needle)` 会直接将探针插入序列,并且比两步操作更加迅速

- 数组 (Array)
	- 如果一个列表只包含数字,那么数组是一个很好的选择,数组比列表效率更高,同样支持可变序列的所有方法
	- 快速存取: `frombytes` 和 `tofile`

- MemoryViews (内存查看对象?)
	- 受 NumPy 和 SciPy 启发产生,可以修改序列中部分内容而不影响其他部分,类似于C语音的指针
	- 大概在大量数据处理时使用可以降低计算复杂度? 个人感觉日常用途不明

- 双端队列 (Double-Ended Queue)
	- 队列的设计目的是为了快速从端点插入或移除数据
	- 双端队列在声明是需要显式声明最大长度,当队列中的元素达到最大长度后继续添加元素会从另一端移除元素
	- 除了双端队列,Python标准库还实现了一些其他队列
		- `queue` 线程安全的单端序列,在达到最大值后会等待移除而不是自动移除
		- `multiprocessing` 提供了支持多进程的队列(
		- `asynio` 异步队列

### Chapter 3 | 字典和集合

- 通用映射类型 (Generic Mapping Types)
	- `collections.abc` (Abstract Base Classes)模块提供了 `Mapping` 和 `MutableMapping` 两个类型,用于规定字典和相似类型的接口
	- 所有的映射类型都要求他们的关键字是可哈希的
		- 可哈希对象 (Hashable)
			- 所有原子级不可变的类型都可以计算哈希值,所以一个仅包含不可变类型的静态集总是可以哈希的,用户定义的类型默认时可哈希的,其哈希值是他们的 `id()`

- 字典
	- 表达方式
		- 从2.7开始字典的声明可以使用递推式构造 `{country: code for code, country in DIAL_CODES}` 其中 `DIAL_CODES = [(86, 'China'), ...]`
	- 通过setdefault处理不存在的关键字
	- defaultdict: 在声明时提供一个可供调用的初始化函数(如list, 会返回一个空列表), 在索引到一个不存在的key时会调用这个函数
	- `__missing__`: 在通过get索引时会自动调用, 处理不存在索引引发的错误
	- 其他字典
		- OrderedDict: 内部元素的顺序会维持插入的顺序
		- ChainMap: 可以将多个映射合并为一个, 如对多个进行查询操作可以用到
		- Counter: 会对每一个出现的key进行计数, 可以用于统计字符串中字符数量
		- UserDict: 用纯Python实现的映射类型, 和普通字典相似
	- 扩展
		- 在对基础字典进行扩展以实现自定义映射类型时, 更推荐使用 UserDict, 因为它是以纯 python 实现的, 扩展起来更加方便, 比起使用dict代码可能更简单

- 不可变映射类型 (Immutable Mappings)
	- 在我们需要维持一些字典内容不被误操作所改变时, 我们可以通过 `MappingProxy` 实现, 向 `MappingProxyType(obj)` 传入一个映射对象, 会返回一个只读映射对象, 这个只读对象会随着被传入的对象变化而变化, 但直接对该只读对象的操作不会生效, 更不会影响到原对象

- 集合
	- 集合是一个在 Python 历史中相对较新的内容, `set` 和 `frozenset` 在 Python 2.6 时被纳入内建类型
	- 集合一个非常常见的功能就是去重, 集合内的所有元素是不重复的, 同时, 集合内的所有元素必须是可哈希的, `set` 本身是不可哈希的, 而 `frozenset` 是可哈希的, 所以可以在 `set` 中包含 `frozenset`
	- 集合支持一些集合论的操作, 集合在记录检索方面具有极大的优势(代码简单且执行速度快), 假设你有两份很长的通讯录, 然后要比较这两份通讯录中重叠的条目数量, 集合就是一个很好的选择: `len(mailing_list_1 & mailing_list_2)`
	- 表达方式
		- `s = {1, 2, ...}` 是一个最基础的声明方式, 注意, 你不能用这种方式生成一个空集合, `{}` 会返回一个字典而不是集合
		- 递推表达式: 和上文说明相似

- 哈希表 (Hash Table)
	- 哈希表是一个稀疏的数组, 在基础数据结构说明中, 哈希表的单元被称作 "buckets", Python 会试图保持至少 1/3 的单元是空的, 所以当这个哈希表变得拥挤时, Python会把他复制到一个新的更大的空间中
	- 要向哈希表中添加一个键值对时, 首先计算出这个键值对中关键字的哈希值, 对于用户自定义类的哈希值默认是它的id, 如果需要修改是否相等的判断依据, 要同时修改对应的hash计算方法, 因为当 `a == b` 时, `hash(a) == hash(b)` 必须成立
	- 前面提到的字典和集合就是基于哈希表建立的, 因此对于键的搜索是十分迅速的
	- 对字典进行空间优化(不推荐): 由于字典是基于哈希表的, 在高效的同时, 对于空间的有一定的浪费, 可以通过修改 `__slots__` 方法, 这个内容会在第九章进行详细讨论, 但如果不能证明对空间的优化是必要的, 请不要这样做, 因为优化总是在牺牲代码的可维护性
	- 哈希表中的元素(这里的元素指不基于哈希表的数据类型, 如元组)内部键值对顺序与插入顺序有关, 不影响哈希值计算, 向一个字典中添加内容可能会改变键值顺序(相当于向哈希表中插入内容)

### Chapter 4 | 文本和字节


<strong>To be Continued...</strong>